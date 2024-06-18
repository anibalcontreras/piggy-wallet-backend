from django.urls import path
from .views import RegisterView, LoginView, UserSearchView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("search/", UserSearchView.as_view(), name="get"),
]
