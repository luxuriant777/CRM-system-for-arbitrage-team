from django.urls import path
from .views import ProspectCreateView, ProspectListView

app_name = "api_prospects"

urlpatterns = [
    path("create/", ProspectCreateView.as_view(), name="prospect-create"),
    path("list/", ProspectListView.as_view(), name="prospect-list"),
]
