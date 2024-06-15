# user_expense_type/urls.py
from django.urls import path
from .views import UserExpenseTypeViewSet

urlpatterns = [
    path(
        "",
        UserExpenseTypeViewSet.as_view({"get": "list", "post": "create"}),
        name="user_expense_type",
    ),
    path(
        "<int:pk>/",
        UserExpenseTypeViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "partial_update"}
        ),
        name="user_expense_type_detail",
    ),
]
