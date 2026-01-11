from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "success": False,
            "error": {
                "status_code": response.status_code,
                "message": response.data.get("detail", "Request failed"),
                "details": response.data
            }
        }, status=response.status_code)

    # Unhandled exceptions (500)
    logger.exception("Unhandled exception", exc_info=exc)

    return Response({
        "success": False,
        "error": {
            "status_code": 500,
            "message": "Internal server error"
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
