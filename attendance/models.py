from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from authentications.models import User
from .choices import STATUS_CHOICES

class Attendance(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=datetime.date.today)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    location = models.CharField(max_length=255, null=True, blank=True)
    
    # Face recognition verification
    verified_by_face = models.BooleanField(default=False)
    face_confidence = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    face_image = models.ImageField(upload_to='attendance_faces/', null=True, blank=True)
    
    # Liveness detection
    liveness_score = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    liveness_checks = models.JSONField(default=dict, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time_in']
        unique_together = ['student', 'date']
        indexes = [
            models.Index(fields=['student', 'date']),
            models.Index(fields=['date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.date} ({self.status})"
    
    @property
    def duration(self):
        if self.time_in and self.time_out:
            from datetime import datetime, date
            time_in_dt = datetime.combine(date.today(), self.time_in)
            time_out_dt = datetime.combine(date.today(), self.time_out)
            duration = time_out_dt - time_in_dt
            return str(duration).split('.')[0]  # Remove microseconds
        return None