from datetime import date
from factory import Faker
from factory.django import DjangoModelFactory

from projects.models import Project, ProjectTimeLog


class ProjectFactory(DjangoModelFactory):
    """Factory class to create Project objects using fake data"""

    class Meta:
        model = Project

    name = Faker("name").generate({})
    description = Faker("text").generate({})


class ProjectTimeLogFactory(DjangoModelFactory):
    """Factory class to create Project Time Log objects using fake data"""

    class Meta:
        model = ProjectTimeLog

    date = date.today()
    start_time = "14:00:00"
    end_time = "18:00:00"
    description = Faker("text").generate({})
