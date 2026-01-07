from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Class, AttendanceSchedule
from .serializers import (
    ClassSerializer,
    AttendanceScheduleSerializer
)
from authentications.permissions import IsAdminOrTeacher


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'teacher']


class AttendanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSchedule.objects.select_related('class_obj')
    serializer_class = AttendanceScheduleSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['day_of_week', 'is_active']
