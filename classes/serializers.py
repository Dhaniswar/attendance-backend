from rest_framework import serializers
from .models import Class, AttendanceSchedule
from users.serializers import UserSerializer


class ClassSerializer(serializers.ModelSerializer):
    teacher_details = UserSerializer(source='teacher', read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = (
            'id', 'name', 'code', 'description',
            'teacher', 'teacher_details',
            'students', 'student_count',
            'start_date', 'end_date',
            'is_active', 'created_at'
        )
        read_only_fields = ('id', 'created_at')

    def get_student_count(self, obj):
        return obj.students.count()


class AttendanceScheduleSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(
        source='get_day_of_week_display',
        read_only=True
    )

    class Meta:
        model = AttendanceSchedule
        fields = (
            'id', 'class_obj', 'day_of_week',
            'day_of_week_display',
            'start_time', 'end_time',
            'is_active'
        )
