from django.db import models
from authentications.models import User


class FaceImage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='face_images'
    )
    image = models.ImageField(upload_to='face_images/')
    encoding = models.JSONField(help_text="Face embedding vector")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Face image for {self.user.email}"
