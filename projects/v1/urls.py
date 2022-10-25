from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register("projects", ProjectView, basename="project")
router.register("projects-time-logs", ProjectTimeLogView, basename="project_time_log")


urlpatterns = router.urls
