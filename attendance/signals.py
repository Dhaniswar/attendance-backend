from django.db.models.signals import post_save
from django.dispatch import receiver
from attendance.models import Attendance
from core.logging.system_logger import send_notification





@receiver(post_save, sender=Attendance)
def attendance_created_handler(sender, instance, created, **kwargs):
    if created:
        # Notify student
        send_notification(
            user=instance.student,
            type='attendance',
            title='Attendance Recorded',
            message=f'Your attendance has been recorded for {instance.date}',
            metadata={
                'status': instance.status,
                'time_in': instance.time_in.isoformat() if instance.time_in else None
            }
        )
        
        # Notify admins/teachers (in production, would send to relevant teachers)
        if instance.created_by and instance.created_by != instance.student:
            send_notification(
                user=instance.created_by,
                type='attendance',
                title='Attendance Marked',
                message=f'Attendance marked for {instance.student.get_full_name()}',
                metadata={
                    'student': instance.student.get_full_name(),
                    'status': instance.status
                }
            )

