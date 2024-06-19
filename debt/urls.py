from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DebtViewSet


urlpatterns = [
    path(
        "",
        DebtViewSet.as_view({"get": "list", "post": "create", "delete": "destroy", "put": "partial_update"}),
        name="debt",
    ),
    path("users/", DebtViewSet.as_view({"get": "users"}), name="debt-users"),
    path("balance/<str:other_user_id>/", DebtViewSet.as_view({"get": "balance"}), name="debt-balance"),
    path("settle/<str:other_user_id>/", DebtViewSet.as_view({"post": "settle"}), name="debt-settle"),
    path("toggle-payment/<str:debt_id>/", DebtViewSet.as_view({"put": "toggle_payment"}), name="debt-toggle-payment"),
]
