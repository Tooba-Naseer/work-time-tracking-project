import string
import random
from copy import deepcopy
from factory import Faker

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserRegistrationTestCase(APITestCase):
    """Test class to test user registration API"""

    def setUp(self):
        self.url = reverse("user_register")
        self.password = Faker("password").generate({})
        self.email = Faker("safe_email").generate({})
        self.first_name = Faker("first_name").generate({})
        self.last_name = Faker("last_name").generate({})

        self.data = {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "confirm_password": self.password,
        }

    def test_register_api(self):
        response = self.client.post(self.url, self.data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response_data)
        self.assertIn("refresh", response_data)
        self.assertIn("id", response_data)
        self.assertEqual(1, User.objects.all().count())

        data = deepcopy(self.data)
        data.pop("password")
        data.pop("confirm_password")
        for field in data:
            self.assertEqual(self.data[field], response_data[field])

        # register user with existing email
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_api_no_email(self):
        data = deepcopy(self.data)
        data.pop("email")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_api_no_password(self):
        data = deepcopy(self.data)
        data.pop("password")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_validations(self):
        data = deepcopy(self.data)

        # max length should not be less than 8 validator
        data["password"] = data["confirm_password"] = "".join(
            random.choices(string.digits, k=4)
        )
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # password should not contain all numeric values validator
        data["password"] = data["confirm_password"] = "".join(
            random.choices(string.digits, k=9)
        )
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_match_password_confirm_password(self):
        data = deepcopy(self.data)
        password = Faker("password").generate({})
        while data["password"] == password:
            password = Faker("password").generate({})
        data["confirm_password"] = password
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
