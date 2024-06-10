from django.urls import path
from .views import ExpenseViewSet, ExpenseGroupedByTypeAndCategoryViewSet

urlpatterns = [
    path(
        "",
        ExpenseViewSet.as_view({"get": "list", "post": "create", "delete": "destroy", "put": "partial_update"}),
        name="expenses",
    ),
    path(
        "grouped/",
        ExpenseGroupedByTypeAndCategoryViewSet.as_view({"get": "list"}),
        name="expenses_grouped",
    ),
]
