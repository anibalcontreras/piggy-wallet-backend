from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DebtViewSet

router = DefaultRouter()
router.register(r"debts", DebtViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
