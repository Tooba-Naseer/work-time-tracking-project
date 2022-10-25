from rest_framework import serializers

from projects.models import Project
from users.v1.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project"""

    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("created_by",)


class ProjectReadOnlySerializer(serializers.ModelSerializer):
    """Read only serializer for Project"""

    class Meta:
        model = Project
        fields = ("id", "name", "description")
