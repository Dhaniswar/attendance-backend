from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'type_display', 'title', 'message',
            'is_read', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_type_display(self, obj):
        return obj.get_type_display()