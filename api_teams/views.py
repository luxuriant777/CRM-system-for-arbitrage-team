from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Team
from .serializers import TeamSerializer
from rest_framework import permissions


class TeamPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # "GET", "HEAD", or "OPTIONS"
            return request.user.has_perm("api_teams.view_team")

        # Map method to permission codename
        method_permissions = {
            "POST": "api_teams.add_team",
            "PUT": "api_teams.change_team",
            "PATCH": "api_teams.change_team",
            "DELETE": "api_teams.delete_team",
        }

        return request.user.has_perm(method_permissions.get(request.method, ""))


class TeamCreateView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]


class TeamDetailView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]


class TeamUpdateView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]


class TeamDeleteView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]
