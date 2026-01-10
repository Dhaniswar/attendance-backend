from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from authentications.permissions import IsAdminOrTeacher, IsSelfOrAdmin
from authentications.models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer
)
from biometrics.serializers import FaceEnrollmentSerializer
from biometrics import face_recognition
from core.logging.system_logger import log_system_event
from notifications.sender import send_notification
from analytics.statistics import get_user_statistics



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'is_active']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsSelfOrAdmin()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrTeacher])
    def enroll_face(self, request, pk=None):
        """Enroll user's face for recognition"""
        user = self.get_object()
        
        serializer = FaceEnrollmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = face_recognition.enroll_face(
                user, 
                serializer.validated_data['images']
            )
            
            log_system_event(
                level='info',
                type='face_recognition',
                message=f'Face enrolled for user {user.email}',
                user=request.user
            )
            
            send_notification(
                user=user,
                type='info',
                title='Face Enrollment Complete',
                message='Your face has been successfully enrolled in the system.',
                metadata={'images_count': len(serializer.validated_data['images'])}
            )
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            log_system_event(
                level='error',
                type='face_recognition',
                message=f'Face enrollment failed for {user.email}: {str(e)}',
                user=request.user
            )
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrTeacher])
    def statistics(self, request):
        """Get user statistics"""
        stats = get_user_statistics()
        return Response(stats)

