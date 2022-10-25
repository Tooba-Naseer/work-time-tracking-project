from django.contrib.auth.models import AbstractUser
from django.db import models

from .user_manager import CustomUserManager
from common.models import TimeStampModel


class User(AbstractUser, TimeStampModel):
    """Model class for custom user model"""

    username = None  # remove default username field
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"  # set email as authentication field
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
