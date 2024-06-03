# budget/urls.py
from django.urls import path
from .views import get_user_budget, set_user_budget, delete_user_budget, update_user_budget

urlpatterns = [
    path('budget/', get_user_budget, name='get_user_budget'),
    path('budget/set', set_user_budget, name='set_user_budget'),
    path('budget/delete', delete_user_budget, name='delete_user_budget'),
    path('budget/update', update_user_budget, name='update_user_budget'),
]
