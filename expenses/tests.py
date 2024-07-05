from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from authentication.models import User
from user_expense_type.models import UserExpenseType
from bankcard.models import BankCard
from authentication.services.cognito_service import CognitoService


class ExpenseViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test@email.com",
            email="test@email.com",
            password="TestPassword1",
            first_name="Test User",
            user_id="389704ef-1e4f-4000-a801-bf887a1c88f2",
        )
        self.user_expense_type = UserExpenseType.objects.create(
            username="389704ef-1e4f-4000-a801-bf887a1c88f2", set_by_user=False, name="Personal"
        )
        self.bankcard = BankCard.objects.create(
            user_id=self.user, account_number=123456, bank_name="Test Bank", card_type="debit"
        )
        self.expense_data = {
            "user_expense_type": self.user_expense_type.id,
            "category": 1,
            "bankcard_id": self.bankcard.id,
            "amount": 100,
            "description": "Test description",
            "username": "389704ef-1e4f-4000-a801-bf887a1c88f2",
        }

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("expenses.views.categorize_expense_description")
    @patch("expenses.views.get_user_id_from_token")
    def test_create(self, mock_get_user_id, mock_categorize, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_categorize.return_value = self.expense_data, None
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.post("/expenses/", self.expense_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 100)

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("expenses.views.categorize_expense_description")
    @patch("expenses.views.get_user_id_from_token")
    def test_list(self, mock_get_user_id, mock_categorize, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_categorize.return_value = self.expense_data, None
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.post("/expenses/", self.expense_data)
        response = self.client.post("/expenses/", self.expense_data)
        response = self.client.get("/expenses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("expenses.views.categorize_expense_description")
    @patch("expenses.views.get_user_id_from_token")
    def test_retrieve(self, mock_get_user_id, mock_categorize, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_categorize.return_value = self.expense_data, None
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.post("/expenses/", self.expense_data)
        response = self.client.get(f"/expenses/{response.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 100)

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("expenses.views.categorize_expense_description")
    @patch("expenses.views.get_user_id_from_token")
    def test_update(self, mock_get_user_id, mock_categorize, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_categorize.return_value = self.expense_data, None
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.post("/expenses/", self.expense_data)
        response = self.client.put(f"/expenses/{response.data['id']}/", {"amount": 200})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 200)

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("expenses.views.categorize_expense_description")
    @patch("expenses.views.get_user_id_from_token")
    def test_delete(self, mock_get_user_id, mock_categorize, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_categorize.return_value = self.expense_data, None
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.post("/expenses/", self.expense_data)
        response = self.client.delete(f"/expenses/{response.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch("authentication.decorators.get_user_id_from_token")
    @patch("expenses.views.categorize_expense_description")
    @patch("expenses.views.get_user_id_from_token")
    def test_grouped(self, mock_get_user_id, mock_categorize, mock_auth_get_user_id):
        mock_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"
        mock_categorize.return_value = self.expense_data, None
        mock_auth_get_user_id.return_value = "389704ef-1e4f-4000-a801-bf887a1c88f2"

        response = self.client.post("/expenses/", self.expense_data)
        response = self.client.post("/expenses/", self.expense_data)
        response = self.client.get("/expenses/grouped/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["Personal"]["Comida"], 200)
