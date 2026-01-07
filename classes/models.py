from django.db import models
from authentications.models import User


class Class(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_classes'
    )
    students = models.ManyToManyField(
        User,
        related_name='classes',
        blank=True
    )

    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"


class AttendanceSchedule(models.Model):
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='schedules'
    )

    day_of_week = models.IntegerField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ]
    )

    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ('class_obj', 'day_of_week')

    def __str__(self):
        return (
            f"{self.class_obj.name} - "
            f"{self.get_day_of_week_display()} "
            f"{self.start_time}-{self.end_time}"
        )
