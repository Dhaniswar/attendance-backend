import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class AttendanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authentication via query parameter or header
        token = self.scope['query_string'].decode().split('token=')[1] if 'token=' in self.scope['query_string'].decode() else None
        
        if not token:
            await self.close(code=4001)  # Custom close code for authentication failure
            return
        
        # Verify token
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            self.scope['user'] = await self.get_user(user_id)
            
            if not self.scope['user']:
                await self.close(code=4001)
                return
        except TokenError:
            await self.close(code=4001)
            return
        
        # Join attendance group
        await self.channel_layer.group_add(
            "attendance_updates",
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"WebSocket connected: {self.scope['user'].email}")
    
    async def disconnect(self, close_code):
        # Leave attendance group
        await self.channel_layer.group_discard(
            "attendance_updates",
            self.channel_name
        )
        logger.info(f"WebSocket disconnected: {close_code}")
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
        except json.JSONDecodeError:
            pass
    
    async def attendance_marked(self, event):
        """Send attendance marked event to client"""
        await self.send(text_data=json.dumps({
            'type': 'attendance_marked',
            'data': event['attendance']
        }))
    
    async def student_registered(self, event):
        """Send student registered event to client"""
        await self.send(text_data=json.dumps({
            'type': 'student_registered',
            'data': event['student']
        }))
    
    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        
        # Authentication
        token = self.scope['query_string'].decode().split('token=')[1] if 'token=' in self.scope['query_string'].decode() else None
        
        if not token:
            await self.close(code=4001)
            return
        
        try:
            access_token = AccessToken(token)
            token_user_id = access_token['user_id']
            
            if int(self.user_id) != token_user_id:
                await self.close(code=4001)
                return
            
            self.scope['user'] = await self.get_user(token_user_id)
            if not self.scope['user']:
                await self.close(code=4001)
                return
        except (TokenError, ValueError):
            await self.close(code=4001)
            return
        
        # Join user-specific notification group
        await self.channel_layer.group_add(
            f"user_{self.user_id}",
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"Notification WebSocket connected for user {self.user_id}")
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user_id}",
            self.channel_name
        )
        logger.info(f"Notification WebSocket disconnected for user {self.user_id}: {close_code}")
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get('type') == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
        except json.JSONDecodeError:
            pass
    
    async def notification(self, event):
        """Send notification to client"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['notification']
        }))
    
    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None