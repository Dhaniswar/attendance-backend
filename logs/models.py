from django.db import models
from authentications.models import User


class SystemLog(models.Model):
    LOG_LEVELS = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('debug', 'Debug'),
    )
    
    LOG_TYPES = (
        ('attendance', 'Attendance'),
        ('face_recognition', 'Face Recognition'),
        ('system', 'System'),
        ('user', 'User'),
        ('security', 'Security'),
    )
    
    level = models.CharField(max_length=20, choices=LOG_LEVELS, default='info')
    type = models.CharField(max_length=50, choices=LOG_TYPES, default='system')
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_level_display()}: {self.message[:50]}..."