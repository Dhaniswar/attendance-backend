from django.contrib import admin
from .models import SystemLog

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'type', 'user', 'ip_address', 'created_at', 'short_message')
    list_filter = ('level', 'type', 'created_at')
    search_fields = ('message', 'user__username', 'ip_address')
    readonly_fields = ('level', 'type', 'message', 'user', 'ip_address', 'metadata', 'created_at')
    ordering = ('-created_at',)
    
    def short_message(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    short_message.short_description = 'Message'