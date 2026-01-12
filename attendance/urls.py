from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, export_attendance

router = DefaultRouter()
router.register('', AttendanceViewSet, basename='attendance')


urlpatterns = [
    path('export/', export_attendance, name='attendance-export'),
    path('', include(router.urls)),
    
]