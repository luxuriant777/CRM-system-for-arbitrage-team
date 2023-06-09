from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/", include("user_management.urls")),
    path("api/", include("customer_management.urls")),
    path("jet/", include("jet.urls", "jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("admin/", admin.site.urls),
]
