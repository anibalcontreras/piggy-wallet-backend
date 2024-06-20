from django.urls import path
from .views import CategoryViewSet

urlpatterns = [
    path("", CategoryViewSet.as_view({"get": "list"}), name="category"),
    path("<int:pk>/", CategoryViewSet.as_view({"get": "retrieve"}), name="category-detail"),
]
