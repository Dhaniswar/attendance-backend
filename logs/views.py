from django.shortcuts import render
from rest_framework import viewsets
from authentications.permissions import IsAdmin
from .models import SystemLog
from .serializers import SystemLogSerializer
from django_filters.rest_framework import DjangoFilterBackend





class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['level', 'type', 'user']