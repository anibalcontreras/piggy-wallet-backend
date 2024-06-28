from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from authentication.services.cognito_service import CognitoService
from authentication.views import ProfileView
from rest_framework.response import Response


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


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/profile/"
        self.data = {"email": "johndoe@example.com", "password": "securepassword123"}

    @patch.object(ProfileView, "get")
    @patch.object(CognitoService, "login_user")
    # Hay que modificar este test o no? Porque retorna first_name, user_id y email
    # De hecho, no se como funcionaba si solo estaba testeando first_name y la response actual es con user_id tmb:
    # {
    #     "user_id": "819ba510-10d1-7014-a98a-0bc46d8e9b5e",
    #     "first_name": "Pedro Alonso"
    # }
    def test_get(self, mock_login_user, mock_get):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_get.return_value = Response(status=status.HTTP_200_OK, data={"first_name": "John Doe"})
        request = self.client.get(self.url)
        request.headers["Authorization"] = "Bearer mock_access_token"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John Doe")
