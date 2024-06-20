from django.urls import path
from .views import ExpenseViewSet, ExpenseGroupedByTypeAndCategoryViewSet

urlpatterns = [
    path(
        "",
        ExpenseViewSet.as_view({"get": "list", "post": "create"}),
        name="expenses",
    ),
    path(
        "<int:pk>/",
        ExpenseViewSet.as_view({"get": "retrieve", "put": "partial_update", "delete": "destroy"}),
        name="expense-detail",
    ),
    path(
        "grouped/",
        ExpenseGroupedByTypeAndCategoryViewSet.as_view({"get": "list"}),
        name="expenses_grouped",
    ),
]
