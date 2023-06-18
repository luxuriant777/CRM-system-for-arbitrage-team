from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Arbitrage teams CRM",
        default_version="v1",
        description="API for CRM tailored to suit the requirements of an arbitrage teams",
        contact=openapi.Contact(email="alexander.kolomoiets@gmail.com"),
        license=openapi.License(name="GNU General Public License v3.0"),
        ),
    public=True,
    permission_classes=[permissions.AllowAny],
    )

urlpatterns = [
    path("", include("html_templates.urls")),
    path("api/users/", include(("api_users.urls", "api_users"), namespace="api_users")),
    path("api/prospects/", include(("api_prospects.urls", "api_prospects"), namespace="api_prospects")),
    path("api/orders/", include(("api_orders.urls", "api_orders"), namespace="api_orders")),
    path("api/teams/", include(("api_teams.urls", "api_teams"), namespace="api_teams")),
    path("jet/", include(("jet.urls", "jet"), namespace="jet")),
    path("jet/dashboard/", include(("jet.dashboard.urls", "jet-dashboard"), namespace="jet-dashboard")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
