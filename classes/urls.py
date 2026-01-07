from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, AttendanceScheduleViewSet

router = DefaultRouter()
router.register('classes', ClassViewSet, basename='class')
router.register('schedules', AttendanceScheduleViewSet, basename='schedule')

urlpatterns = router.urls
