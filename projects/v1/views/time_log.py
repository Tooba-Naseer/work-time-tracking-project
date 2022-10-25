from django_filters import rest_framework as rest_filters
from django.db.models import DurationField, ExpressionWrapper, F, Sum

from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from projects.v1.serializers import ProjectTimeLogSerializer
from projects.models import ProjectTimeLog
from ..permissions import IsTimeLogOwnerPermission
from ..filters import ProjectTimeLogFilter


class ProjectTimeLogView(viewsets.ModelViewSet):
    """View for Project Time Log"""

    queryset = (
        ProjectTimeLog.objects.all()
        .select_related("user", "project")
        .annotate(
            duration=ExpressionWrapper(
                F("end_time") - F("start_time"), output_field=DurationField()
            )
        )
    )
    serializer_class = ProjectTimeLogSerializer
    permission_classes = (IsAuthenticated, IsTimeLogOwnerPermission)
    filter_backends = (
        rest_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = ProjectTimeLogFilter
    search_fields = (
        "^project__name",
    )  # provide starts_with search filter on project name
    ordering_fields = (
        "date",
        "created_at",
        "project",
    )  # provide both asc and desc ordering on specified fields
    ordering = ("-date", "-created_at")  # default ordering

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="total-time-spent")
    def total_time_spent(self, request, *args, **kwargs):
        """
        This API calculates total time spent using queryset.
        Eg: If we want to see that how much total time a specific user spent in last two months on that specific project.
        We can find out that using this API.
        """

        total_time = self.filter_queryset(super().get_queryset()).aggregate(
            total_time=Sum("duration")
        )

        return Response(
            {"total_time_spent": str(total_time.get("total_time"))},
            status=status.HTTP_200_OK,
        )
