from rest_framework import serializers
from django.utils import timezone
from .models import Attendance
from users.serializers import UserSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)
    duration = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = (
            'id', 'student', 'student_details', 'date',
            'time_in', 'time_out', 'status', 'status_display',
            'location', 'verified_by_face', 'face_confidence',
            'liveness_score', 'duration', 'created_at'
        )
        read_only_fields = ('id', 'created_at')

    def get_duration(self, obj):
        return str(obj.duration) if obj.duration else None

    def validate(self, attrs):
        if self.instance is None:
            student = attrs.get('student')
            date = attrs.get('date', timezone.now().date())
            if Attendance.objects.filter(student=student, date=date).exists():
                raise serializers.ValidationError(
                    "Attendance already marked for this date."
                )
        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
