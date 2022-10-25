from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import *


urlpatterns = [
    path("register", UserRegistrationView.as_view(), name="user_register"),
    path("login", UserLoginView.as_view(), name="user_login"),
    path("token/refresh", TokenRefreshView.as_view(), name="refresh_token"),
]
