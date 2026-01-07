from django.contrib import admin
from .models import FaceImage


@admin.register(FaceImage)
class FaceImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('user__email', 'user__student_id')
    readonly_fields = ('created_at',)
