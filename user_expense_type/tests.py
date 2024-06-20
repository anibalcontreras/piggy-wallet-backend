from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from authentication.services.cognito_service import CognitoService
from user_expense_type.views import UserExpenseTypeViewSet
from rest_framework.response import Response


class UserExpenseTypeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = UserExpenseTypeViewSet()
        self.user_expense_type_data = {
            "name": "Viajes",
            "description": "Gastos incurridos en viajes",
            "set_by_user": True,
        }

    @patch.object(UserExpenseTypeViewSet, "create")
    @patch.object(CognitoService, "login_user")
    def test_create(self, mock_login_user, mock_create):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_create.return_value = Response(status=status.HTTP_201_CREATED, data=self.user_expense_type_data)

        request = self.client.post("/user_expense_type/", self.user_expense_type_data)
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.post("/user_expense_type/", self.user_expense_type_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Viajes")

    @patch.object(UserExpenseTypeViewSet, "list")
    @patch.object(CognitoService, "login_user")
    def test_list(self, mock_login_user, mock_list):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_list.return_value = Response(status=status.HTTP_200_OK, data=self.user_expense_type_data)

        request = self.client.get("/user_expense_type/")
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.get("/user_expense_type/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Viajes")

    @patch.object(UserExpenseTypeViewSet, "destroy")
    @patch.object(CognitoService, "login_user")
    def test_destroy(self, mock_login_user, mock_destroy):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_destroy.return_value = Response(status=status.HTTP_204_NO_CONTENT)

        request = self.client.delete("/user_expense_type/1/")
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.delete("/user_expense_type/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(UserExpenseTypeViewSet, "partial_update")
    @patch.object(CognitoService, "login_user")
    def test_partial_update(self, mock_login_user, mock_partial_update):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        new_user_expense_type_data = {
            "name": "Viajes",
            "description": "Gastos incurridos en viajes por placer",
            "set_by_user": True,
        }
        mock_partial_update.return_value = Response(status=status.HTTP_200_OK, data=new_user_expense_type_data)

        request = self.client.put("/user_expense_type/1/", {"description": "Gastos incurridos en viajes por placer"})
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.put("/user_expense_type/1/", {"description": "Gastos incurridos en viajes por placer"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Gastos incurridos en viajes por placer")
