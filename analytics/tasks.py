from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from authentications.models import User
from notifications.models import   Notification
from core.logging.system_logger import log_system_event


@shared_task
def send_daily_attendance_report():
    """Send daily attendance report to admins"""
    from analytics.statistics import get_attendance_statistics
    
    today = timezone.now().date()
    stats = get_attendance_statistics(today)
    
    admins = User.objects.filter(role='admin', is_active=True)
    
    for admin in admins:
        Notification.objects.create(
            user=admin,
            type='info',
            title='Daily Attendance Report',
            message=f"Today's attendance: {stats['present_attendance']}/{stats['total_attendance']} ({stats['attendance_rate']:.1f}%)",
            metadata=stats
        )
    
    log_system_event(
        level='info',
        type='system',
        message='Sent daily attendance reports'
    )
    
    return "Daily reports sent"

