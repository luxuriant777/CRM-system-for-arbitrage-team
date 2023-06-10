from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserListView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("list/", UserListView.as_view(), name="user-list"),
]
