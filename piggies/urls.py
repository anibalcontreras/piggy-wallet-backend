from django.urls import path
from .views import PiggiesViewSet, NotPiggiesViewSet

urlpatterns = [
    path(
        "",
        PiggiesViewSet.as_view({"get": "list", "post": "create"}),
        name="piggies",
    ),
    path(
        "users/",
        NotPiggiesViewSet.as_view({"get": "users"}),
        name="not_piggies",
    ),
]
