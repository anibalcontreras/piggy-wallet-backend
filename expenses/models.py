from django.db import models
from user_expense_type.models import UserExpenseType
from categories.models import Category


class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.UUIDField()
    user_expense_type = models.ForeignKey(UserExpenseType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # cambiar cuando exista el modelo de bankcard
    bankcard_id = models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
