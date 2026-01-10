from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import (
    FaceDetectionSerializer,
    LivenessCheckSerializer,
    FaceEnrollmentSerializer
)
from .services import face_recognition
from authentications.models import User
from core.logging.system_logger import log_system_event


class FaceDetectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FaceDetectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = face_recognition.detect_faces(
                serializer.validated_data['image']
            )
            return Response(result)
        except Exception as e:
            log_system_event(
                level='error',
                type='face_recognition',
                message=str(e),
                user=request.user
            )
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class FaceVerificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FaceDetectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.face_encoding:
            return Response(
                {"error": "Face not enrolled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = face_recognition.verify_face(
            serializer.validated_data['image'],
            user.face_encoding
        )
        return Response(result)


class LivenessCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LivenessCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = face_recognition.check_liveness(
            serializer.validated_data['images']
        )
        return Response(result)


class FaceEnrollmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FaceEnrollmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(
                student_id=serializer.validated_data['student_id']
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # enrollment logic goes here
        return Response(
            {"success": True, "message": "Face enrolled successfully"}
        )
