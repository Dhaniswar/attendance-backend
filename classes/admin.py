from django.contrib import admin
from .models import Class, AttendanceSchedule


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code', 'teacher',
        'start_date', 'end_date', 'is_active'
    )
    list_filter = ('is_active', 'teacher')
    search_fields = ('name', 'code')
    filter_horizontal = ('students',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AttendanceSchedule)
class AttendanceScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'class_obj', 'day_of_week',
        'start_time', 'end_time', 'is_active'
    )
    list_filter = ('day_of_week', 'is_active')
