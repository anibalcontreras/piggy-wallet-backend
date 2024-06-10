# budget/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Budget
import json

class BudgetTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.budget = Budget.objects.create(user=self.user, amount=100)

    def test_get_user_budget(self):
        url = reverse('get_user_budget')
        response = self.client.get(url, {'user_id': self.user.id}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'user_id': self.user.id, 'amount': self.budget.amount})

    def test_set_user_budget(self):
        url = reverse('set_user_budget')
        user = get_user_model().objects.create_user(username='testuser2', password='password')
        response = self.client.post(url, json.dumps({'user_id': user.id, 'amount': 200}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Budget created successfully.'})
        self.assertEqual(Budget.objects.get(user=user).amount, 200)

    def test_delete_user_budget(self):
        url = reverse('delete_user_budget')
        response = self.client.delete(url, json.dumps({'user_id': self.user.id}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Budget deleted successfully', 'user_id': self.user.id})
        self.assertFalse(Budget.objects.filter(user=self.user).exists())

    def test_update_user_budget(self):
        url = reverse('update_user_budget')
        response = self.client.patch(url, json.dumps({'user_id': self.user.id, 'amount': 300}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'user_id': self.user.id, 'budget': 300})
        self.assertEqual(Budget.objects.get(user=self.user).amount, 300)
