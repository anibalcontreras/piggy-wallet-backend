from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category
from .views import CategoryViewSet
from authentication.services.cognito_service import CognitoService
from rest_framework.response import Response
from .serializers import CategorySerializer


class CategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_credentials = {
            "AuthenticationResult": {"AccessToken": "mock_access_token", "IdToken": "mock_id_token"}
        }

    @patch.object(CategoryViewSet, "list")
    @patch.object(CognitoService, "login_user")
    def test_list_categories(self, mock_login_user, mock_list):
        mock_login_user.return_value = self.user_credentials
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        mock_list.return_value = Response(status=status.HTTP_200_OK, data=serializer.data)

        response = self.client.get("/categories/")
        response.headers["Authorization"] = "Bearer mock_access_token"

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @patch.object(CategoryViewSet, "retrieve")
    @patch.object(CognitoService, "login_user")
    def test_retrieve_category(self, mock_login_user, mock_retrieve):
        mock_login_user.return_value = self.user_credentials
        category = Category.objects.get(id=1)
        serializer = CategorySerializer(category)
        mock_retrieve.return_value = Response(status=status.HTTP_200_OK, data=serializer.data)

        response = self.client.get("/categories/1/")
        response.headers["Authorization"] = "Bearer mock_access_token"

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @patch.object(CategoryViewSet, "retrieve")
    @patch.object(CognitoService, "login_user")
    def test_category_not_found(self, mock_login_user, mock_retrieve):
        mock_login_user.return_value = self.user_credentials
        mock_retrieve.return_value = Response(status=status.HTTP_404_NOT_FOUND)

        response = self.client.get("/categories/999/")
        response.headers["Authorization"] = "Bearer mock_access_token"

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
