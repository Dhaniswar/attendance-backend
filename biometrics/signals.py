from django.db.models.signals import  pre_save
from django.dispatch import receiver
from authentications.models import User



@receiver(pre_save, sender=User)
def update_face_encoding_version(sender, instance, **kwargs):
    if instance.face_encoding and not instance.face_encoding_version:
        from django.conf import settings
        instance.face_encoding_version = settings.FACE_RECOGNITION_MODEL