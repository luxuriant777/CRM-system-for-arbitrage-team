from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("html_templates.urls")),
    path("api/users/", include(("api_users.urls", "api_users"), namespace="api_users")),
    path("api/leads/", include(("api_leads.urls", "api_leads"), namespace="api_leads")),
    path("api/orders/", include(("api_orders.urls", "api_orders"), namespace="api_orders")),
    path("api/teams/", include(("api_teams.urls", "api_teams"), namespace="api_teams")),
    path("jet/", include(("jet.urls", "jet"), namespace="jet")),
    path("jet/dashboard/", include(("jet.dashboard.urls", "jet-dashboard"), namespace="jet-dashboard")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
