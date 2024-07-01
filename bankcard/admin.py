from django.contrib import admin
from .models import BankCard


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "account_number",
        "bank_name",
        "card_type",
        "created_at",
        "updated_at",
    )
