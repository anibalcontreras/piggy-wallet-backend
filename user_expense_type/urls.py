# user_expense_type/urls.py
from django.urls import path
from .views import get_user_expense_types, get_user_expense_type_by_name, create_user_expense_type, update_user_expense_type, delete_user_expense_type

urlpatterns = [
    path('get', get_user_expense_types, name='get_user_expense_types'),
    path('get/<str:name>', get_user_expense_type_by_name, name='get_user_expense_type_by_name'),
    path('set', create_user_expense_type, name='create_user_expense_type'),
    path('update/<str:name>', update_user_expense_type, name='update_user_expense_type'),
    path('delete/<str:name>', delete_user_expense_type, name='delete_user_expense_type'),
]
