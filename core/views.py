from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Health check endpoint"""
        from django.db import connection
        
        try:
            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            # Check Redis connection
            from django.core.cache import cache
            cache.set('health_check', 'ok', 10)
            cache_result = cache.get('health_check') == 'ok'
            
            # Check face recognition system
            face_recognition_ok = hasattr(face_recognition, 'model_name')
            
            return Response({
                'status': 'healthy',
                'database': 'connected',
                'cache': 'connected' if cache_result else 'disconnected',
                'face_recognition': 'ready' if face_recognition_ok else 'not_ready',
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)