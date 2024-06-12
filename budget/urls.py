# budget/urls.py
from django.urls import path
from .views import BudgetViewSet

urlpatterns = [
    path(
        "",
        BudgetViewSet.as_view({"get": "list", "post": "create", "delete": "destroy", "put": "partial_update"}),
        name="budget",
    ),
]
