from datetime import date
from datetime import datetime

from django.db import models

from common.models import TimeStampModel
from users.models import User


class Project(TimeStampModel):
    """Model class for storing projects"""

    name = models.CharField(max_length=500, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects"
    )


class ProjectTimeLog(TimeStampModel):
    """Model class for storing work time spent on the projects by the user"""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="time_logs"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_time")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)

    @property
    def time_spent(self):
        """Calculate total time spent in hh:mm:ss"""

        return datetime.combine(date.today(), self.end_time) - datetime.combine(
            date.today(), self.start_time
        )
