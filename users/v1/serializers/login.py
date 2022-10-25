from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .register import RegistrationSerializer


class LoginSerializer(serializers.Serializer):
    """Serializer for User Login"""

    email = serializers.EmailField()
    password = serializers.CharField()

    def to_representation(self, instance):
        return RegistrationSerializer(instance).data

    def create(self, validated_data):
        """Authenticate the user"""

        user = authenticate(
            email=validated_data.get("email").lower(),
            password=validated_data.get("password"),
        )

        if not user:
            raise AuthenticationFailed

        return user
