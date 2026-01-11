from django.db.models.signals import post_save
from django.dispatch import receiver
from authentications.models import User
from logs.models import SystemLog
from notifications.sender import send_notification


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        # Send welcome notification
        send_notification(
            user=instance,
            type='info',
            title='Welcome to Attendance System',
            message=f'Welcome {instance.get_full_name()}! Your account has been created successfully.',
            metadata={'role': instance.role}
        )
        
        # Log user creation
        SystemLog.objects.create(
            level='info',
            type='user',
            message=f'User {instance.email} created with role {instance.role}',
            user=instance
        )

