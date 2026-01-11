import logging
from logs.models import SystemLog

logger = logging.getLogger(__name__)


def log_system_event(level, type, message, user=None, ip_address=None, metadata=None):
    """Log system events"""
    try:
        SystemLog.objects.create(
            level=level,
            type=type,
            message=message,
            user=user,
            ip_address=ip_address,
            metadata=metadata or {}
        )
    except Exception as e:
        logger.error(f"Failed to log system event: {str(e)}")