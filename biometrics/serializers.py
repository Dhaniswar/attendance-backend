from rest_framework import serializers
from .models import FaceImage



class FaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceImage
        fields = ['id', 'image', 'encoding', 'is_verified', 'created_at']
        read_only_fields = ['id', 'encoding', 'is_verified', 'created_at']


class FaceDetectionSerializer(serializers.Serializer):
    image = serializers.CharField(
        required=True,
        help_text="Base64 encoded image"
    )
    location = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate_image(self, value):
        if not value.startswith('data:image/'):
            raise serializers.ValidationError(
                "Invalid image format. Must be base64 encoded image."
            )
        return value


class LivenessCheckSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.CharField(),
        min_length=3,
        help_text="List of base64 encoded images"
    )

    def validate_images(self, value):
        for img in value:
            if not img.startswith('data:image/'):
                raise serializers.ValidationError("Invalid image format.")
        return value


class FaceEnrollmentSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    images = serializers.ListField(
        child=serializers.CharField(),
        min_length=3,
        max_length=10
    )
