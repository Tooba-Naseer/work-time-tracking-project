import copy
from datetime import datetime, timedelta, date
from factory import Faker

from rest_framework.test import APITestCase
from rest_framework import status

from projects.models import ProjectTimeLog
from .factory import ProjectFactory, ProjectTimeLogFactory
from users.tests.factory import UserFactory


class ProjectTimeLogTestCases(APITestCase):
    """Test class to test Create, Update, Retrieve, List, Get total time spent and Delete time log APIs"""

    def setUp(self):
        self.user = UserFactory()
        self.url = "/api/v1/projects-time-logs"
        self.client.force_login(self.user)
        project = ProjectFactory(created_by=self.user, name="Project_test")

        self.data = {
            "project": project.id,
            "description": Faker("text").generate({}),
            "date": "2022-10-25",
            "start_time": "09:00:00",
            "end_time": "15:00:00",
        }

    def test_create_time_log_api(self):
        response = self.client.post(self.url, self.data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        time_log = ProjectTimeLog.objects.all().first()

        self.assertEqual(ProjectTimeLog.objects.all().count(), 1)
        self.assertEqual(response_data["date"], str(time_log.date))
        self.assertEqual(response_data["start_time"], str(time_log.start_time))
        self.assertEqual(response_data["end_time"], str(time_log.end_time))
        self.assertEqual(response_data["project"]["id"], time_log.project_id)
        self.assertEqual(response_data["description"], time_log.description)
        self.assertEqual(response_data["user"]["id"], time_log.user_id)
        self.assertIn("created_at", response_data)
        self.assertIn("updated_at", response_data)
        self.assertIn("id", response_data)

    def test_create_time_log_api_date_validation(self):
        data = copy.deepcopy(self.data)
        future_datetime = datetime.today() + timedelta(days=20)
        data["date"] = future_datetime.date()

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_time_log_api_time_validation(self):
        data = copy.deepcopy(self.data)
        data["start_time"] = "12:00:00"
        data["end_time"] = "10:00:00"
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        project_1 = ProjectFactory(created_by=self.user, name="Project1")
        project_2 = ProjectFactory(created_by=self.user, name="Project2")
        ProjectTimeLogFactory(
            project=project_1,
            user=self.user,
            start_time="08:00:00",
            end_time="11:00:00",
        )
        ProjectTimeLogFactory(
            project=project_1,
            user=self.user,
            start_time="13:00:00",
            end_time="15:00:00",
        )
        ProjectTimeLogFactory(
            project=project_2,
            user=self.user,
            start_time="16:00:00",
            end_time="18:00:00",
        )

        # test time clash validation
        data = copy.deepcopy(self.data)
        data["start_time"] = "12:00:00"
        data["end_time"] = "14:00:00"
        data["date"] = date.today()
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_project_time_log_api(self):
        project_1 = ProjectFactory(created_by=self.user, name="Project1")
        project_2 = ProjectFactory(created_by=self.user, name="Project2")
        time_log = ProjectTimeLogFactory(project=project_1, user=self.user)
        url = f"/api/v1/projects-time-logs/{time_log.id}"
        data = {
            "description": Faker("text").generate({}),
            "start_time": "12:00:00",
            "end_time": "15:00:00",
            "date": "2022-09-09",
            "project": project_2.id,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        time_log.refresh_from_db()
        self.assertEqual(data["description"], time_log.description)
        self.assertEqual(data["start_time"], str(time_log.start_time))
        self.assertEqual(data["end_time"], str(time_log.end_time))
        self.assertEqual(data["date"], str(time_log.date))
        self.assertEqual(data["project"], time_log.project_id)

    def test_retrieve_project_time_log_api(self):
        project = ProjectFactory(created_by=self.user, name="Project1")
        time_log = ProjectTimeLogFactory(project=project, user=self.user)
        url = f"/api/v1/projects-time-logs/{time_log.id}"

        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["description"], time_log.description)
        self.assertEqual(response_data["start_time"], str(time_log.start_time))
        self.assertEqual(response_data["end_time"], str(time_log.end_time))
        self.assertEqual(response_data["date"], str(time_log.date))
        self.assertEqual(response_data["project"]["id"], time_log.project_id)
        self.assertIn("id", response_data)
        self.assertIn("duration", response_data)

    def test_get_all_projects_time_logs_api(self):
        user = UserFactory(email="testuser@gmail.com")
        project_1 = ProjectFactory(name="Project1", created_by=self.user)
        project_2 = ProjectFactory(name="Project2", created_by=user)
        project_3 = ProjectFactory(name="Project3", created_by=user)
        time_log_1 = ProjectTimeLogFactory(project=project_1, user=self.user)
        time_log_2 = ProjectTimeLogFactory(project=project_2, user=user)
        time_log_3 = ProjectTimeLogFactory(
            project=project_3, user=self.user, date="2022-09-09"
        )

        response = self.client.get(self.url)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["count"], 3)
        self.assertEqual(response_data["results"][0]["id"], time_log_2.id)
        self.assertEqual(response_data["results"][0]["date"], str(time_log_2.date))
        self.assertEqual(response_data["results"][1]["id"], time_log_1.id)
        self.assertEqual(
            response_data["results"][1]["start_time"], str(time_log_1.start_time)
        )
        self.assertEqual(response_data["results"][2]["id"], time_log_3.id)
        self.assertEqual(response_data["results"][2]["date"], str(time_log_3.date))
        self.assertEqual(
            response_data["results"][2]["end_time"], str(time_log_3.end_time)
        )
        self.assertIn("duration", response_data["results"][2])

    def test_delete_project_time_log_api(self):
        project = ProjectFactory(created_by=self.user, name="Project1")
        time_log = ProjectTimeLogFactory(project=project, user=self.user)
        url = f"/api/v1/projects-time-logs/{time_log.id}"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        time_log = ProjectTimeLogFactory(
            project=project, user=UserFactory(email="testuser@gmail.com")
        )

        url = f"/api/v1/projects-time-logs/{time_log.id}"
        response = self.client.delete(url)

        # test permission that user should be able to delete his own logs
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
