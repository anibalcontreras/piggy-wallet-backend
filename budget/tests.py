from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import BudgetViewSet
from .models import Budget
from django.contrib.auth.models import User
from unittest.mock import patch


class BudgetViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.viewset = BudgetViewSet()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.budget = Budget.objects.create(user=self.user, amount=100)

    @patch("budget.views.get_user_id_from_token")
    def test_list(self, mock_get_user_id_from_token):
        mock_get_user_id_from_token.return_value = self.user.id

        request = self.factory.get("/")
        response = self.viewset.list(request)
        self.assertEqual(response.status_code, 200)

    @patch("budget.views.get_user_id_from_token")
    def test_create(self, mock_get_user_id_from_token):
        mock_get_user_id_from_token.return_value = self.user.id

        request_data = {"amount": 200}
        request = self.factory.post("/", request_data, format="json")
        response = self.viewset.create(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Budget.objects.count(), 2)

    @patch("budget.views.get_user_id_from_token")
    def test_destroy(self, mock_get_user_id_from_token):
        mock_get_user_id_from_token.return_value = self.user.id

        request = self.factory.delete("/")
        response = self.viewset.destroy(request, pk=self.budget.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Budget.objects.count(), 0)

    @patch("budget.views.get_user_id_from_token")
    def test_partial_update(self, mock_get_user_id_from_token):
        mock_get_user_id_from_token.return_value = self.user.id

        request_data = {"amount": 150}
        request = self.factory.patch("/", request_data, format="json")
        response = self.viewset.partial_update(request, pk=self.budget.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Budget.objects.get(pk=self.budget.id).amount, 150)
