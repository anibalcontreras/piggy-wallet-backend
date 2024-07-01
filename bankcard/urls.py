from django.urls import path
from .views import BankCardViewSet

urlpatterns = [
    path(
        "",
        BankCardViewSet.as_view({"get": "list", "post": "create"}),
        name="bankcard",
    ),
    path(
        "<int:pk>/",
        BankCardViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "partial_update"}),
        name="individual",
    ),
]
