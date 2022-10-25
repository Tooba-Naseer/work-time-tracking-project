from copy import deepcopy
from factory import Faker

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .factory import UserFactory


class UserLoginTestCase(APITestCase):
    """Test Class to test user login API"""

    def setUp(self):
        self.url = reverse("user_login")
        self.user = UserFactory()
        self.password = Faker("password").generate({})
        self.user.set_password(self.password)
        self.user.save()

        self.data = {"email": self.user.email, "password": self.password}

    def test_login_api(self):
        response = self.client.post(self.url, self.data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response_data)
        self.assertIn("refresh", response_data)
        self.assertIn("id", response_data)
        self.assertEqual(self.user.first_name, response_data["first_name"])
        self.assertEqual(self.user.last_name, response_data["last_name"])
        self.assertEqual(self.user.email, response_data["email"])

    def test_login_api_wrong_email(self):
        data = deepcopy(self.data)
        email = Faker("safe_email").generate({})
        while data["email"] == email:
            email = Faker("safe_email").generate({})
        data["email"] = email
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_api_no_email(self):
        data = deepcopy(self.data)
        data.pop("email")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_api_no_password(self):
        data = deepcopy(self.data)
        data.pop("password")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
