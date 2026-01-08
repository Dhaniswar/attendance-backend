from django.shortcuts import render
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.response import Response
from attendance.models import Attendance
from authentications.permissions import IsAdminOrTeacher
from core.logging.system_logger import get_user_statistics, get_attendance_statistics









@api_view(['GET'])
@permission_classes([IsAdminOrTeacher])
def dashboard_statistics(request):
    """Get dashboard statistics"""
    from django.db.models import Count, Q, Avg
    
    # User statistics
    user_stats = get_user_statistics()
    
    # Today's attendance
    today_stats = get_attendance_statistics()
    
    # Overall attendance rate
    total_attendance = Attendance.objects.count()
    present_attendance = Attendance.objects.filter(status='present').count()
    
    if total_attendance > 0:
        overall_rate = (present_attendance / total_attendance) * 100
    else:
        overall_rate = 0
    
    # Recent activity
    recent_attendance = Attendance.objects.select_related('student').order_by('-created_at')[:10]
    recent_activity = []
    
    for att in recent_attendance:
        recent_activity.append({
            'type': 'attendance',
            'message': f'{att.student.get_full_name()} marked attendance',
            'time': att.created_at,
            'data': {
                'student': att.student.get_full_name(),
                'status': att.get_status_display(),
                'time': att.time_in.isoformat() if att.time_in else None
            }
        })
    
    return Response({
        'user_statistics': user_stats,
        'today_attendance': today_stats,
        'overall_attendance_rate': overall_rate,
        'recent_activity': recent_activity,
        'face_recognition_model': face_recognition.model_name,
        'face_confidence_threshold': face_recognition.threshold
    })
