from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from .views import (
    index,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    ProspectListView,
    ProspectDetailView,
    ProspectCreateView,
    ProspectUpdateView,
    ProspectDeleteView,
    CustomUserListView,
    CustomUserDetailView,
    CustomUserCreateView,
    CustomUserUpdateView,
    CustomUserDeleteView,
)

app_name = "html_templates"

urlpatterns = [
    path("", index, name="index"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    path("prospects/", ProspectListView.as_view(), name="prospect-list"),
    path("prospects/<int:pk>/", ProspectDetailView.as_view(), name="prospect-detail"),
    path("prospects/create/", ProspectCreateView.as_view(), name="prospect-create"),
    path("prospects/<int:pk>/update/", ProspectUpdateView.as_view(), name="prospect-update"),
    path("prospects/<int:pk>/delete/", ProspectDeleteView.as_view(), name="prospect-delete"),
    path("users/", CustomUserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", CustomUserDetailView.as_view(), name="user-detail"),
    path("users/create/", CustomUserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", CustomUserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", CustomUserDeleteView.as_view(), name="user-delete"),
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='html_templates:login'), name="logout"),
    path("admin/logout/", auth_views.LogoutView.as_view(next_page='html_templates:login'), name="logout"),
    path("accounts/profile/", RedirectView.as_view(url="/"), name="profile"),
]
