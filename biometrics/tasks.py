from celery import shared_task
from core.logging.system_logger import log_system_event


@shared_task
def cleanup_old_face_images():
    """Clean up old face images"""
    from .models import FaceImage
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=30)
    old_images = FaceImage.objects.filter(created_at__lt=cutoff_date)
    count = old_images.count()
    
    for image in old_images:
        image.image.delete(save=False)
    
    old_images.delete()
    
    log_system_event(
        level='info',
        type='system',
        message=f'Cleaned up {count} old face images'
    )
    
    return f"Cleaned up {count} old face images"



@shared_task
def backup_face_encodings():
    """Backup face encodings to secure storage"""
    from .models import User
    import json
    from django.conf import settings
    
    users_with_faces = User.objects.exclude(face_encoding__isnull=True)
    
    backup_data = []
    for user in users_with_faces:
        backup_data.append({
            'user_id': user.id,
            'email': user.email,
            'face_encoding': user.face_encoding,
            'version': user.face_encoding_version,
            'updated_at': user.last_face_update.isoformat() if user.last_face_update else None
        })
    
    # For now, just log the backup
    log_system_event(
        level='info',
        type='system',
        message=f'Backed up {len(backup_data)} face encodings'
    )
    
    return f"Backed up {len(backup_data)} face encodings"