from django.db import models
from django.conf import settings


class Piggies(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="user_id", related_name="origin"
    )
    piggy = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="user_id", related_name="friend"
    )
