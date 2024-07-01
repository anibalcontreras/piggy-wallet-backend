from django.db import models
from django.conf import settings

from user_expense_type.models import UserExpenseType
from categories.models import Category
from bankcard.models import BankCard


class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="user_id")
    user_expense_type = models.ForeignKey(UserExpenseType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    bankcard_id = models.ForeignKey(BankCard, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
