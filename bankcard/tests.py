from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from authentication.services.cognito_service import CognitoService
from rest_framework.response import Response
from .views import BankCardViewSet


class BankCardViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = BankCardViewSet()
        self.card = {
            "account_number": 44467861,
            "bank_name": "Super Bank",
            "card_type": "credit",
        }

    @patch.object(BankCardViewSet, "create")
    @patch.object(CognitoService, "login_user")
    def test_create(self, mock_login_user, mock_create):
        mock_login_user.return_value = {
            "AuthenticationResult": {"access_token": "mock_access_token", "id_token": "mock_id_token"}
        }
        mock_create.return_value = Response(status=status.HTTP_201_CREATED, data=self.card)

        request = self.client.post("/bankcard/", self.card)
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.post("/bankcard/", self.card)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["account_number"], 44467861)

    @patch.object(BankCardViewSet, "list")
    @patch.object(CognitoService, "login_user")
    def test_list(self, mock_login_user, mock_list):
        mock_login_user.return_value = {
            "AuthenticationResult": {"access_token": "mock_access_token", "id_token": "mock_id_token"}
        }
        mock_list.return_value = Response(status=status.HTTP_200_OK, data=[self.card])

        request = self.client.get("/bankcard/")
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.get("/bankcard/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["account_number"], 44467861)

    @patch.object(BankCardViewSet, "retrieve")
    @patch.object(CognitoService, "login_user")
    def test_retrieve(self, mock_login_user, mock_retrieve):
        mock_login_user.return_value = {
            "AuthenticationResult": {"access_token": "mock_access_token", "id_token": "mock_id_token"}
        }
        mock_retrieve.return_value = Response(status=status.HTTP_200_OK, data=self.card)

        request = self.client.get("/bankcard/1/")
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.get("/bankcard/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_number"], 44467861)

    @patch.object(BankCardViewSet, "destroy")
    @patch.object(CognitoService, "login_user")
    def test_destroy(self, mock_login_user, mock_destroy):
        mock_login_user.return_value = {
            "AuthenticationResult": {"access_token": "mock_access_token", "id_token": "mock_id_token"}
        }
        mock_destroy.return_value = Response(status=status.HTTP_204_NO_CONTENT)

        request = self.client.delete("/bankcard/1/")
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.delete("/bankcard/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(BankCardViewSet, "partial_update")
    @patch.object(CognitoService, "login_user")
    def test_partial_update(self, mock_login_user, mock_partial_update):
        mock_login_user.return_value = {
            "AuthenticationResult": {"access_token": "mock_access_token", "id_token": "mock_id_token"}
        }
        update = {
            "account_number": 44467861,
            "bank_name": "Super Earth Bank",
            "card_type": "credit",
        }
        mock_partial_update.return_value = Response(status=status.HTTP_200_OK, data=update)

        request = self.client.put("/bankcard/1/", {"bank_name": "Super Earth Bank"})
        request.headers["Authorization"] = "Bearer mock_access_token"

        response = self.client.put("/bankcard/1/", {"bank_name": "Super Earth Bank"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_number"], 44467861)
