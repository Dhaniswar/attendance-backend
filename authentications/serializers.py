from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.state import token_backend
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token["email"] = user.email
        token["is_verified"] = user.is_verified
        token["is_admin"] = user.is_superuser
        token["username"] = user.email
        token["role"] = user.role
        token["student_id"] = user.student_id or ""
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Wrap user info in 'user' key
        user_data = {
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "username": self.user.email,
            "is_verified": self.user.is_verified,
            "is_admin": self.user.is_superuser,
            "role": self.user.role,
            "student_id": self.user.student_id or "",
        }

        data.update({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data  # <-- frontend expects this key
        })

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        decoded_payload = token_backend.decode(refresh.token, verify=True)

        user_data = {
            "email": decoded_payload.get("email", ""),
            "first_name": decoded_payload.get("first_name", ""),
            "last_name": decoded_payload.get("last_name", ""),
            "username": decoded_payload.get("username", ""),
            "is_verified": decoded_payload.get("is_verified", False),
            "is_admin": decoded_payload.get("is_admin", False),
            "role": decoded_payload.get("role", ""),
            "student_id": decoded_payload.get("student_id", ""),
        }

        data.update({
            "refresh": str(refresh),
            "user": user_data
        })
        return data