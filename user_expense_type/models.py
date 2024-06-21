from django.db import models
from django.conf import settings


class UserExpenseType(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.UUIDField()
    name = models.CharField(max_length=70, default="Personal")
    description = models.CharField(max_length=255, blank=True, null=True)
    set_by_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
