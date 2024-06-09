from django.db import models
from django.conf import settings

class UserExpenseType(models.Model):
    id = models.AutoField(primary_key=True)  # ID serial no nulo
    user_id = models.IntegerField()
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, default="Personal")
    description = models.CharField(max_length=255, blank=True, null=True)
    set_by_user = models.BooleanField(default=False)
    category_name = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"
