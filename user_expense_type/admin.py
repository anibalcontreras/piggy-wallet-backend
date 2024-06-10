from django.contrib import admin
from .models import UserExpenseType


@admin.register(UserExpenseType)
class UserExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "created_at", "updated_at")
    search_fields = ("username", "name", "category_name")
