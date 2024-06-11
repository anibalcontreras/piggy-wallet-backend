from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from authentication.services.cognito_service import CognitoService
from rest_framework.response import Response
from .views import ExpenseViewSet, ExpenseGroupedByTypeAndCategoryViewSet


class ExpenseViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = ExpenseViewSet()
        self.expense = {
            "expense_type_id": 1,
            "category_id": 1,
            "bankcard_id": 1,
            "amount": 100,
        }

    @patch.object(ExpenseViewSet, "create")
    @patch.object(CognitoService, "login_user")
    def test_create(self, mock_login_user, mock_create):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_create.return_value = Response(status=status.HTTP_201_CREATED, data=self.expense)

        request = self.client.post("/expenses/", self.expense)
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.post("/expenses/", self.expense)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 100)

    @patch.object(ExpenseViewSet, "list")
    @patch.object(CognitoService, "login_user")
    def test_list(self, mock_login_user, mock_list):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_list.return_value = Response(status=status.HTTP_200_OK, data=self.expense)

        request = self.client.get("/expenses/")
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.get("/expenses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 100)

    @patch.object(ExpenseViewSet, "destroy")
    @patch.object(CognitoService, "login_user")
    def test_destroy(self, mock_login_user, mock_destroy):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_destroy.return_value = Response(status=status.HTTP_204_NO_CONTENT)

        request = self.client.delete("/expenses/")
        request.headers["Authorization"] = "Bearer mock_access_token"
        request.body = {"id": 1}

        response = self.client.delete("/expenses/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(ExpenseViewSet, "partial_update")
    @patch.object(CognitoService, "login_user")
    def test_partial_update(self, mock_login_user, mock_partial_update):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        new_expense = {
            "expense_type_id": 1,
            "category_id": 1,
            "bankcard_id": 1,
            "amount": 200,
        }
        mock_partial_update.return_value = Response(status=status.HTTP_200_OK, data=new_expense)

        request = self.client.put("/expenses/", {"amount": 200})
        request.headers["Authorization"] = "Bearer mock_access_token"
        request.body = {"id": 1}

        response = self.client.put("/expenses/", {"amount": 200})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 200)


class ExpenseGroupedByTypeAndCategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = ExpenseGroupedByTypeAndCategoryViewSet()
        self.expense = {
            "expense_type_id": 1,
            "category_id": 1,
            "bankcard_id": 1,
            "amount": 100,
        }
        self.expenses_grouped = {"Personal": {"Comida": 100}}

    @patch.object(ExpenseGroupedByTypeAndCategoryViewSet, "list")
    @patch.object(CognitoService, "login_user")
    def test_list(self, mock_login_user, mock_list):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_list.return_value = Response(status=status.HTTP_200_OK, data=self.expenses_grouped)

        request = self.client.get("/expenses/grouped/")
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.get("/expenses/grouped/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Personal", response.data)
        self.assertIn("Comida", response.data["Personal"])
        self.assertEqual(response.data["Personal"]["Comida"], 100)
