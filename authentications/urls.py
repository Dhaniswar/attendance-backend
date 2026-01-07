from django.urls import path
from .views import CustomTokenRefreshView, CustomTokenObtainPairView


urlpatterns = [
    path('token/access/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]


