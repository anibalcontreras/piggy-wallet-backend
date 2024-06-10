# user_expense_type/urls.py
from django.urls import path
from .views import UserExpenseTypeViewSet

urlpatterns = [
    path(
        "",
        UserExpenseTypeViewSet.as_view({"get": "list", "post": "create", "delete": "destroy", "put": "partial_update"}),
        name="user_expense_type",
    ),
]
