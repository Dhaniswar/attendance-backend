from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/attendance/', consumers.AttendanceConsumer.as_asgi()),
    path('ws/notifications/<int:user_id>/', consumers.NotificationConsumer.as_asgi()),
]


