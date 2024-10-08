# budget/models.py
from django.db import models
from django.conf import settings


class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.UUIDField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
