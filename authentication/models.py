from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    phone = models.CharField(max_length=15, blank=True)
