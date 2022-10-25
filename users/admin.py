from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Customize admin portal for user model"""

    readonly_fields = ("password",)
    list_display = ("id", "email", "first_name", "last_name", "is_active")
    search_fields = ("id", "email", "first_name", "last_name")
