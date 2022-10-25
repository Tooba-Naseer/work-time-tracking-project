from django.contrib import admin

from projects.models import Project, ProjectTimeLog


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Customize admin portal for project model"""

    list_display = ("id", "name", "created_by")
    search_fields = ("id", "name")


@admin.register(ProjectTimeLog)
class ProjectAdmin(admin.ModelAdmin):
    """Customize admin portal for project time log model"""

    list_display = ("id", "project", "user", "date", "start_time", "end_time")
    search_fields = ("id", "user__email", "project__name")
