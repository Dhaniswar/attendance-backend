from django.urls import path, include
from .views import HealthCheckView



urlpatterns = [

    path('health/', HealthCheckView.as_view(), name='health_check'),

]