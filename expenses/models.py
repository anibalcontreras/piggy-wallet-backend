from django.db import models


class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.UUIDField()
    expense_type_id = models.IntegerField()
    category_id = models.IntegerField()
    bankcard_id = models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
