import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification

logger = logging.getLogger(__name__)




def send_notification(user, type, title, message, metadata=None):
    """Send notification to user"""
    try:
        notification = Notification.objects.create(
            user=user,
            type=type,
            title=title,
            message=message,
            metadata=metadata or {}
        )
        
        # Send WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "notification",
                "notification": {
                    "id": notification.id,
                    "type": notification.type,
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": notification.created_at.isoformat(),
                }
            }
        )
        
        return notification
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return None


