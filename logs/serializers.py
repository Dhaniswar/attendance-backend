from rest_framework import serializers
from users.serializers import UserSerializer
from .models import SystemLog



class SystemLogSerializer(serializers.ModelSerializer):
    level_display = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = SystemLog
        fields = [
            'id', 'level', 'level_display', 'type', 'type_display',
            'message', 'user', 'user_details', 'ip_address',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_level_display(self, obj):
        return obj.get_level_display()
    
    def get_type_display(self, obj):
        return obj.get_type_display()