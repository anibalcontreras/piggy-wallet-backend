from django.conf import settings
from django.db import models


class Debt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="debts")
    debtor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owed_debts")
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
