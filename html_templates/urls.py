from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView

from .views import (
    index,
    LeadListView,
    LeadDetailView,
    LeadCreateView,
    LeadUpdateView,
    LeadDeleteView,
    CustomUserListView,
    CustomUserDetailView,
    CustomUserCreateView,
    CustomUserUpdateView,
    CustomUserDeleteView,
    toggle_lead_assign,
)

app_name = "html_templates"

urlpatterns = [
    path("", index, name="index"),
    path("leads/", LeadListView.as_view(), name="lead-list"),
    path("leads/<int:pk>/", LeadDetailView.as_view(), name="lead-detail"),
    path("leads/create/", LeadCreateView.as_view(), name="lead-create"),
    path(
        "lead/<int:pk>/toggle-assign/",
        toggle_lead_assign,
        name="toggle-lead-assign",
    ),
    path(
        "leads/<int:pk>/update/", LeadUpdateView.as_view(), name="lead-update"
    ),
    path(
        "leads/<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-delete"
    ),
    path("users/", CustomUserListView.as_view(), name="user-list"),
    path(
        "users/<int:pk>/", CustomUserDetailView.as_view(), name="user-detail"
    ),
    path("users/create/", CustomUserCreateView.as_view(), name="user-create"),
    path(
        "users/<int:pk>/update/",
        CustomUserUpdateView.as_view(),
        name="user-update",
    ),
    path(
        "users/<int:pk>/delete/",
        CustomUserDeleteView.as_view(),
        name="user-delete",
    ),
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='html_templates:login'), name="logout"),
    path("admin/logout/", auth_views.LogoutView.as_view(next_page='html_templates:login'), name="logout"),
    path("accounts/profile/", RedirectView.as_view(url="/"), name="profile"),
]
