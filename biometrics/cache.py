import logging
from django.utils import timezone
from django.core.cache import cache


logger = logging.getLogger(__name__)



def cache_face_embedding(user_id, embedding):
    """Cache face embedding for faster verification"""
    cache_key = f"face_embedding_{user_id}"
    cache.set(cache_key, embedding, timeout=3600)  # Cache for 1 hour


def get_cached_face_embedding(user_id):
    """Get cached face embedding"""
    cache_key = f"face_embedding_{user_id}"
    return cache.get(cache_key)

