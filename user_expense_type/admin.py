from django.contrib import admin
from .models import UserExpenseType

@admin.register(UserExpenseType)
class UserExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "category_name", "created_at", "updated_at")
    search_fields = ("username", "name", "category_name")
    list_filter = ("category_name",)
    ordering = ("-created_at",)
