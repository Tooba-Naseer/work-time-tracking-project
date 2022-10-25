from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget

from projects.models import ProjectTimeLog


class ProjectTimeLogFilter(filters.FilterSet):
    """Filter Set class for project time log model"""

    date = filters.DateFromToRangeFilter(widget=RangeWidget(attrs={"type": "date"}))

    class Meta:
        model = ProjectTimeLog
        fields = ("date", "project", "user")
