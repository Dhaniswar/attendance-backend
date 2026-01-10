import logging
from django.utils import timezone
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from authentications.models import User
from notifications.models import Notification
from logs.models import SystemLog

logger = logging.getLogger(__name__)


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