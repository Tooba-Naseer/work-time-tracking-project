from rest_framework import generics, permissions

from users.v1.serializers import LoginSerializer


class UserLoginView(generics.CreateAPIView):
    """View for User Login"""

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
