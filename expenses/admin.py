from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "amount",
        "user_expense_type_name",
        "category_name",
        "bankcard_id",
        "created_at",
        "updated_at",
    )

    def user_expense_type_name(self, obj):
        return obj.user_expense_type.name

    user_expense_type_name.short_description = "User Expense Type"

    def category_name(self, obj):
        return obj.category.name

    category_name.short_description = "Category"
