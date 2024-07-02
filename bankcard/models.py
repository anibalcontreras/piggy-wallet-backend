from django.db import models
from django.conf import settings


class BankCard(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="user_id")
    account_number = models.IntegerField()
    bank_name = models.CharField(max_length=128)
    card_type = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
