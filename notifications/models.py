from django.db import models
from authentications.models import User
from .choices import NOTIFICATION_TYPE_CHOICES


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('attendance', 'Attendance'),
        ('system', 'System'),
        ('alert', 'Alert'),
        ('info', 'Information'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"