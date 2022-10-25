from factory import Faker

from rest_framework.test import APITestCase
from rest_framework import status

from projects.models import Project
from .factory import ProjectFactory
from users.tests.factory import UserFactory


class ProjectTestCases(APITestCase):
    """Test class to test Create, Update, Retrieve, List and Delete Project APIs"""

    def setUp(self):
        self.user = UserFactory()
        self.url = "/api/v1/projects"
        self.client.force_login(self.user)

        self.data = {
            "name": Faker("name").generate({}),
            "description": Faker("text").generate({}),
        }

    def test_create_project_api(self):
        response = self.client.post(self.url, self.data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        project = Project.objects.all().first()

        self.assertEqual(Project.objects.all().count(), 1)
        self.assertEqual(response_data["name"], project.name)
        self.assertEqual(response_data["description"], project.description)
        self.assertEqual(response_data["created_by"]["id"], project.created_by_id)
        self.assertIn("created_at", response_data)
        self.assertIn("updated_at", response_data)
        self.assertIn("id", response_data)

    def test_update_project_api(self):
        project = ProjectFactory(created_by=self.user)
        url = f"/api/v1/projects/{project.id}"
        data = {
            "name": Faker("name").generate({}),
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        project.refresh_from_db()

        self.assertEqual(data["name"], project.name)

    def test_retrieve_project_api(self):
        project = ProjectFactory(created_by=self.user)
        url = f"/api/v1/projects/{project.id}"

        response = self.client.get(url)
        response_data = response.data

        self.assertEqual(response_data["name"], project.name)
        self.assertEqual(response_data["description"], project.description)
        self.assertEqual(response_data["created_by"]["id"], project.created_by_id)
        self.assertIn("created_at", response_data)
        self.assertIn("updated_at", response_data)
        self.assertIn("id", response_data)

    def test_get_all_projects_api(self):
        user = UserFactory(email="testuser@gmail.com")
        project_1 = ProjectFactory(name="Project1", created_by=self.user)
        project_2 = ProjectFactory(name="Project2", created_by=user)
        project_3 = ProjectFactory(name="Project3", created_by=user)

        response = self.client.get(self.url)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["count"], 3)
        self.assertEqual(response_data["results"][0]["id"], project_3.id)
        self.assertEqual(response_data["results"][0]["name"], project_3.name)
        self.assertEqual(response_data["results"][1]["id"], project_2.id)
        self.assertEqual(response_data["results"][1]["name"], project_2.name)
        self.assertEqual(response_data["results"][2]["id"], project_1.id)
        self.assertEqual(response_data["results"][2]["name"], project_1.name)
        self.assertEqual(
            response_data["results"][2]["description"], project_1.description
        )

    def test_delete_project_api(self):
        project = ProjectFactory(created_by=self.user)
        url = f"/api/v1/projects/{project.id}"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # try deleting the object again, should return 404 error code
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
