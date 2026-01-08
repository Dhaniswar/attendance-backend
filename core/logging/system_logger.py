import logging
from django.utils import timezone
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from authentications.models import User
from .models import SystemLog, Notification

logger = logging.getLogger(__name__)


def log_system_event(level, type, message, user=None, ip_address=None, metadata=None):
    """Log system events"""
    try:
        SystemLog.objects.create(
            level=level,
            type=type,
            message=message,
            user=user,
            ip_address=ip_address,
            metadata=metadata or {}
        )
    except Exception as e:
        logger.error(f"Failed to log system event: {str(e)}")


def send_notification(user, type, title, message, metadata=None):
    """Send notification to user"""
    try:
        notification = Notification.objects.create(
            user=user,
            type=type,
            title=title,
            message=message,
            metadata=metadata or {}
        )
        
        # Send WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "notification",
                "notification": {
                    "id": notification.id,
                    "type": notification.type,
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": notification.created_at.isoformat(),
                }
            }
        )
        
        return notification
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return None


def get_user_statistics():
    """Get user statistics"""
    total_students = User.objects.filter(role='student', is_active=True).count()
    total_teachers = User.objects.filter(role='teacher', is_active=True).count()
    
    return {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_users': total_students + total_teachers
    }


def get_attendance_statistics(date=None):
    """Get attendance statistics for a date"""
    from attendance.models import Attendance
    
    if date is None:
        date = timezone.now().date()
    
    total_attendance = Attendance.objects.filter(date=date).count()
    present_attendance = Attendance.objects.filter(date=date, status='present').count()
    
    if total_attendance > 0:
        attendance_rate = (present_attendance / total_attendance) * 100
    else:
        attendance_rate = 0
    
    return {
        'date': date,
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'attendance_rate': attendance_rate
    }


def validate_image_format(image_data):
    """Validate image format from base64 string"""
    if not image_data.startswith('data:image/'):
        return False
    
    # Check for common image formats
    valid_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp']
    for fmt in valid_formats:
        if f'image/{fmt}' in image_data:
            return True
    
    return False


def cache_face_embedding(user_id, embedding):
    """Cache face embedding for faster verification"""
    cache_key = f"face_embedding_{user_id}"
    cache.set(cache_key, embedding, timeout=3600)  # Cache for 1 hour


def get_cached_face_embedding(user_id):
    """Get cached face embedding"""
    cache_key = f"face_embedding_{user_id}"
    return cache.get(cache_key)


def export_attendance_to_excel(start_date, end_date):
    """Export attendance data to Excel"""
    import pandas as pd
    from io import BytesIO
    from attendance.models import Attendance
    
    # Get attendance data
    attendance_qs = Attendance.objects.filter(
        date__range=[start_date, end_date]
    ).select_related('student').order_by('date', 'student__student_id')
    
    # Convert to DataFrame
    data = []
    for att in attendance_qs:
        data.append({
            'Student ID': att.student.student_id,
            'Student Name': att.student.get_full_name(),
            'Date': att.date,
            'Time In': att.time_in,
            'Time Out': att.time_out,
            'Status': att.get_status_display(),
            'Location': att.location or '',
            'Verified by Face': 'Yes' if att.verified_by_face else 'No',
            'Face Confidence': att.face_confidence or 0,
            'Liveness Score': att.liveness_score or 0,
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Attendance', index=False)
        
        # Add summary sheet
        summary_data = {
            'Metric': ['Total Records', 'Start Date', 'End Date', 'Export Date'],
            'Value': [
                len(df),
                start_date,
                end_date,
                timezone.now().date()
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    return output


def calculate_attendance_percentage(student, start_date, end_date):
    """Calculate attendance percentage for a student"""
    from attendance.models import Attendance
    
    total_days = (end_date - start_date).days + 1
    present_days = Attendance.objects.filter(
        student=student,
        date__range=[start_date, end_date],
        status='present'
    ).count()
    
    if total_days > 0:
        percentage = (present_days / total_days) * 100
    else:
        percentage = 0
    
    return {
        'student': student.get_full_name(),
        'student_id': student.student_id,
        'start_date': start_date,
        'end_date': end_date,
        'total_days': total_days,
        'present_days': present_days,
        'percentage': percentage
    }