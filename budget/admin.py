# budget/admin.py
from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("username", "amount", "created_at", "updated_at")
    search_fields = ("username", "amount")
