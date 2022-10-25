from factory import Faker
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    """Factory class to create User objects using fake data"""

    class Meta:
        model = User

    email = Faker("safe_email").generate({})
    first_name = Faker("first_name").generate({})
    last_name = Faker("last_name").generate({})
