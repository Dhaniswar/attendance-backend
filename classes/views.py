from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from attendance_backend.pagination import CustomPagination

from .models import Class, AttendanceSchedule
from .serializers import (
    ClassSerializer,
    AttendanceScheduleSerializer
)
from authentications.permissions import IsAdminOrTeacher


class ClassViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'teacher']


class AttendanceScheduleViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = AttendanceSchedule.objects.select_related('class_obj')
    serializer_class = AttendanceScheduleSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['day_of_week', 'is_active']
