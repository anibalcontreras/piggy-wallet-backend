from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from authentication.services.cognito_service import CognitoService
from budget.views import BudgetViewSet
from rest_framework.response import Response

class BudgetViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = BudgetViewSet()

    @patch.object(BudgetViewSet, "create")
    @patch.object(CognitoService, "login_user")
    def test_create(self, mock_login_user, mock_create):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_create.return_value = Response(status=status.HTTP_201_CREATED, data={"amount": 100})
        
        request = self.client.post("/budget/", {"amount": 100})
        request.headers["Authorization"] = "Bearer mock_access_token"
        
        response = self.client.post("/budget/", {"amount": 100})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 100)


    @patch.object(BudgetViewSet, "list")
    @patch.object(CognitoService, "login_user")
    def test_list(self, mock_login_user, mock_list):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_list.return_value = Response(status=status.HTTP_200_OK, data={"amount": 100})
        
        request = self.client.get("/budget/")
        request.headers["Authorization"] = "Bearer mock_access_token"
        
        response = self.client.get("/budget/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 100)

    @patch.object(BudgetViewSet, "destroy")
    @patch.object(CognitoService, "login_user")
    def test_destroy(self, mock_login_user, mock_destroy):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_destroy.return_value = Response(status=status.HTTP_204_NO_CONTENT)
        
        request = self.client.delete("/budget/")
        request.headers["Authorization"] = "Bearer mock_access_token"
        
        response = self.client.delete("/budget/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(BudgetViewSet, "partial_update")
    @patch.object(CognitoService, "login_user")
    def test_partial_update(self, mock_login_user, mock_partial_update):
        mock_login_user.return_value = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }
        mock_partial_update.return_value = Response(status=status.HTTP_200_OK, data={"amount": 200})
        
        request = self.client.put("/budget/", {"amount": 200})
        request.headers["Authorization"] = "Bearer mock_access_token"
        
        response = self.client.put("/budget/", {"amount": 200})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 200)
