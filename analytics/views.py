from django.shortcuts import render
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.response import Response
from attendance.models import Attendance
from authentications.permissions import IsAdminOrTeacher
from analytics.statistics import get_user_statistics, get_attendance_statistics
from biometrics import face_recognition
from django.db.models import Count
from django.utils.dateparse import parse_date
from attendance.models import Attendance









@api_view(['GET'])
@permission_classes([IsAdminOrTeacher])
def dashboard_statistics(request):
    """Get dashboard statistics"""
    
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






@api_view(['GET'])
@permission_classes([IsAdminOrTeacher])
def attendance_heatmap(request):
    """Return count of attendance grouped by date"""

    start_date = parse_date(request.GET.get('start_date'))
    end_date = parse_date(request.GET.get('end_date'))

    qs = Attendance.objects.all()

    if start_date and end_date:
        qs = qs.filter(date__range=[start_date, end_date])

    data = (
        qs.values('date')
          .annotate(count=Count('id'))
          .order_by('date')
    )

    return Response({
        'start_date': start_date,
        'end_date': end_date,
        'data': list(data)
    })
