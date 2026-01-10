from django.urls import path, include
from . import views



urlpatterns = [
    # Statistics and dashboard
    path('dashboard/statistics/', views.dashboard_statistics, name='dashboard_statistics'),
    
]