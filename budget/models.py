# budget/models.py
from django.db import models
from django.conf import settings
import uuid


class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.UUIDField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s budget: {self.amount}"
