from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.v1.serializers import RegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """View for User Registration"""

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
