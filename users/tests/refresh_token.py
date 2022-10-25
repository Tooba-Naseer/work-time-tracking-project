from copy import deepcopy
from factory import Faker

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .factory import UserFactory


class RefreshTokenTestCase(APITestCase):
    """Test Class to test refresh token API"""

    def setUp(self):
        self.url = reverse("refresh_token")
        self.user = UserFactory()
        self.user.set_password(Faker("password").generate({}))
        self.user.save()

        self.data = {"refresh": str(RefreshToken.for_user(self.user))}

    def test_refresh_token_api(self):
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_invalid_token(self):
        data = deepcopy(self.data)
        data["refresh"] = Faker("pystr").generate({})
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
