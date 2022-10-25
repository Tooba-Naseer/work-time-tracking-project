from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to set email as authentication field
    instead of username
    """

    def create_user(self, email, password, **extra_fields):
        """Create and save user with given email and password"""

        if not email:
            raise ValueError("Users must have an email")
        user = self.model(email=email.lower(), **extra_fields)
        # creates a hashed password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with given email and password"""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
