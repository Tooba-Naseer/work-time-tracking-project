import copy

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for User Registration"""

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate the incoming data"""

        if User.objects.filter(email__iexact=data.get("email")).exists():
            raise serializers.ValidationError(
                "User with this email address already exists."
            )

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                "Password and confirm password should be same."
            )
        # apply AUTH_PASSWORD_VALIDATORS
        validate_password(data.get("password"))

        return data

    def to_representation(self, instance):
        """Override to_representation and add jwt in the json response"""

        data = super().to_representation(instance)

        # create tokens for user
        refresh = RefreshToken.for_user(instance)
        data.update({"refresh": str(refresh), "access": str(refresh.access_token)})

        return data

    def create(self, validated_data):
        """Create the user"""

        extra_fields = copy.deepcopy(validated_data)
        extra_fields.pop("email")
        extra_fields.pop("confirm_password")
        extra_fields.pop("password")
        user = User.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            **extra_fields
        )

        return user

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
        )
