from django.urls import path
from .views import (
    FaceDetectionView,
    FaceVerificationView,
    LivenessCheckView,
    FaceEnrollmentView
)

urlpatterns = [
    path('detect/', FaceDetectionView.as_view()),
    path('verify/', FaceVerificationView.as_view()),
    path('liveness/', LivenessCheckView.as_view()),
    path('enroll/', FaceEnrollmentView.as_view()),
]
