from django.shortcuts import render
from rest_framework import viewsets

from attendance_backend.pagination import CustomPagination
from .models import Notification
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import NotificationSerializer
from rest_framework import permissions


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = CustomPagination
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'success': True})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'success': True})
