from django.contrib import admin
from .models import Debt


class DebtAdmin(admin.ModelAdmin):
    list_display = ("user", "debtor", "amount", "is_paid", "created_at", "updated_at")
    list_filter = ("is_paid", "created_at", "updated_at")
    search_fields = ("user__username", "debtor__username", "amount")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Debt, DebtAdmin)
