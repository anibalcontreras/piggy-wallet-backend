from django.contrib import admin
from .models import Piggies


@admin.register(Piggies)
class PiggiesAdmin(admin.ModelAdmin):
    list_display = (
        "user_first_name",
        "piggy_first_name",
    )

    def user_first_name(self, obj):
        return obj.username.first_name

    user_first_name.short_description = "User First Name"

    def piggy_first_name(self, obj):
        return obj.piggy.first_name

    piggy_first_name.short_description = "Piggy First Name"
