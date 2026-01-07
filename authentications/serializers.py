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
        # Add custom claims
        token["email"] = user.email
        token["is_verified"] = user.is_verified
        token["is_admin"] = user.is_superuser
        token["username"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        data.update({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": self.user.email,
            "is_verified": self.user.is_verified,
            "is_admin": self.user.is_superuser,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "username": self.user.email,
        })
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        decoded_payload = token_backend.decode(refresh.token, verify=True)
        data["refresh"] = str(refresh)
        
        data.update({
            "is_admin": decoded_payload.get("is_admin", False),
            "is_verified": decoded_payload.get("is_verified", False),
            "email": decoded_payload.get("email", ""),
            "phone": decoded_payload.get("phone", ""),
        })
        return data