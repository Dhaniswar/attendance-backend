from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'date', 'status',
        'verified_by_face', 'created_by', 'created_at'
    )
    list_filter = ('status', 'verified_by_face', 'date')
    search_fields = ('student__email', 'student__student_id')
    readonly_fields = ('created_at', 'updated_at')
