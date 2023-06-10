from django.urls import path
from .views import LeadCreateView, LeadListView

app_name = "api_leads"

urlpatterns = [
    path("create/", LeadCreateView.as_view(), name="lead-create"),
    path("list/", LeadListView.as_view(), name="lead-list"),
]
