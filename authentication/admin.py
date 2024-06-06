from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Status"), {"fields": ("enabled",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "phone",
        "user_id",
        "enabled",
        "created_at",
        "updated_at",
    )
    search_fields = ("username", "first_name", "last_name", "email", "phone", "user_id")
    ordering = ("username",)


admin.site.register(User, UserAdmin)
