from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DebtViewSet


urlpatterns = [
    path(
        "",
        DebtViewSet.as_view({"get": "list", "post": "create", "delete": "destroy", "put": "partial_update"}),
        name="debt",
    ),
]
