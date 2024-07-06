from unittest.mock import patch
from rest_framework.test import APIClient, APITestCase
from authentication.models import User
from rest_framework import status


class PiggiesViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test@email.com",
            email="test@email.com",
            password="TestPassword1",
            first_name="Test User",
            user_id="389704ef-1e4f-4000-a801-bf887a1c88f2",
        )
        self.piggy = User.objects.create_user(
            username="piggy@email.com",
            email="piggy@email.com",
            password="TestPassword1",
            first_name="Test Piggy",
            user_id="389704ef-1e4f-4000-a801-bf887a1c88f3",
        )
        self.not_piggy = User.objects.create_user(
            username="not_piggy@email.com",
            email="not_piggy@email.com",
            password="TestPassword1",
            first_name="Test Not Piggy",
            user_id="389704ef-1e4f-4000-a801-bf887a1c88f4",
        )
        self.piggies_data = {
            "piggy": self.piggy.user_id,
        }

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("piggies.views.get_user_id_from_token")
    def test_integration_create_piggies_then_list(self, mock_get_user_id, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.post("/piggies/", self.piggies_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/piggies/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_id"], self.piggy.user_id)

        response = self.client.get("/piggies/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_id"], self.not_piggy.user_id)

        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f3"

        response = self.client.get("/piggies/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_id"], self.user.user_id)

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("piggies.views.get_user_id_from_token")
    def test_integration_list_not_piggies_then_create_piggies(self, mock_get_user_id, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.get("/piggies/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["user_id"], self.piggy.user_id)
        self.assertEqual(response.data[1]["user_id"], self.not_piggy.user_id)

        response = self.client.post("/piggies/", self.piggies_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/piggies/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_id"], self.not_piggy.user_id)
