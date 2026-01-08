from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')
router.register(r'classes', views.ClassViewSet, basename='class')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'system-logs', views.SystemLogViewSet, basename='systemlog')

urlpatterns = [
    # Statistics and dashboard
    path('dashboard/statistics/', views.dashboard_statistics, name='dashboard_statistics'),
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    
    # Include router URLs
    path('', include(router.urls)),
]