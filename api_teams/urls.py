from django.urls import path
from .views import (TeamCreateView, TeamListView, TeamDetailView, 
                    TeamUpdateView, TeamDeleteView)

urlpatterns = [
    path("create/", TeamCreateView.as_view(), name="teams-create"),
    path("list/", TeamListView.as_view(), name="teams-list"),
    path("detail/<int:pk>/", TeamDetailView.as_view(), name="teams-detail"),
    path("update/<int:pk>/", TeamUpdateView.as_view(), name="teams-update"),
    path("delete/<int:pk>/", TeamDeleteView.as_view(), name="teams-delete"),
]
