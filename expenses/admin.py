from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("username", "amount", "expense_type_id", "category_id", "bankcard_id", "created_at", "updated_at")
    search_fields = ("username", "expense_type_id", "category_id")
