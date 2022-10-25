from django_filters import rest_framework as rest_filters

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from projects.v1.serializers import ProjectSerializer
from projects.models import Project
from ..permissions import IsProjectOwnerPermission


class ProjectView(viewsets.ModelViewSet):
    """View for Project"""

    queryset = Project.objects.all().select_related("created_by")
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsProjectOwnerPermission)
    filter_backends = (
        rest_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ("created_by",)  # provides filter on created_by (id) field
    search_fields = ("^name",)  # provide starts_with search filter on project name
    ordering_fields = (
        "created_at",
        "name",
    )  # provide both asc and desc ordering on specified fields
    ordering = ("-created_at",)  # default ordering

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
