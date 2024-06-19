from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response
from authentication.services.cognito_service import CognitoService


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/register/"
        self.data = {
            "name": "John Doe",
            "phone": "+1234567890",
            "email": "johndoe@example.com",
            "password": "securepassword123#",
        }

    @patch.object(CognitoService, "register_user")
    def test_register_user_success(self, mock_register_user):
        mock_register_user.return_value = None
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully")

    @patch.object(CognitoService, "register_user")
    def test_register_user_failure(self, mock_register_user):
        mock_register_user.side_effect = Exception("Registration failed")
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Registration failed")


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/login/"
        self.data = {"email": "johndoe@example.com", "password": "securepassword123"}

    @patch.object(CognitoService, "login_user")
    def test_login_user_success(self, mock_login_user):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["access_token"], "mock_access_token")
        self.assertEqual(response.data["id_token"], "mock_id_token")

    @patch.object(CognitoService, "login_user")
    def test_login_user_failure(self, mock_login_user):
        mock_login_user.side_effect = Exception("Login failed")
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Login failed")


class UserSearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/search/"
        self.mock_cognito_users = [
            {"Username": "616bc590-8031-7079-8afc-aabb63979373",
             "Email": "vicente.cruz@aurous.cl",
             "Name": "Vini Cruz"},
            {"Username": "019bf590-2001-7040-53f7-07c94de20228",
             "Email": "vcrb@uc.cl",
             "Name": "Vicente Cruz"},
            {"Username": "f1dbc570-b081-7084-7d18-02985b1e8986",
             "Email": "vicruz8@gmail.com",
             "Name": "Vinicius Junior"}
        ]

    @patch.object(CognitoService, "login_user")
    @patch.object(CognitoService, "list_users")
    def test_create(self, mock_login_user, mock_list_users):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_list_users.return_value = Response(status=status.HTTP_201_CREATED, data=self.mock_cognito_users)

        request = self.client.get(self.url)
        request.headers["Authorization"] = "Bearer mock_access_token"

        # response = self.client.get(self.url)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data, self.mock_cognito_users)
