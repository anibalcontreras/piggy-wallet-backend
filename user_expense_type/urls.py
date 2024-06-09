# user_expense_type/urls.py
from django.urls import path
from .views import get_user_expense_types, get_user_expense_type_by_name, create_user_expense_type, update_user_expense_type, delete_user_expense_type

urlpatterns = [
    path('user_expense_type/', get_user_expense_types, name='get_user_expense_types'),
    path('user_expense_type/<str:name>/', get_user_expense_type_by_name, name='get_user_expense_type_by_name'),
    path('user_expense_type/set', create_user_expense_type, name='create_user_expense_type'),
    path('user_expense_type/update/<str:name>/', update_user_expense_type, name='update_user_expense_type'),
    path('user_expense_type/delete/<str:name>/', delete_user_expense_type, name='delete_user_expense_type'),
]
