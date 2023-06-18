from drf_yasg import openapi
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from crm_arbitrage.utils import get_authorization_parameter
from .models import Team
from .serializers import TeamSerializer
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema


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

    @swagger_auto_schema(
        operation_description="Create a team",
        request_body=TeamSerializer,
        responses={
            201: openapi.Response(
                description="Team created successfully",
                schema=TeamSerializer,
            ),
            400: "Bad Request",
        },
        manual_parameters=[
            get_authorization_parameter(),
        ],
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    @swagger_auto_schema(
        operation_description="List all teams",
        responses={
            200: openapi.Response(
                description="OK",
                schema=TeamSerializer(many=True),
            ),
            401: "Unauthorized",
        },
        manual_parameters=[
            get_authorization_parameter(),
        ],
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TeamDetailView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    @swagger_auto_schema(
        operation_description="Retrieve a team by ID",
        responses={
            200: openapi.Response(
                description="OK",
                schema=TeamSerializer,
            ),
            404: "Not Found",
        },
        manual_parameters=[
            get_authorization_parameter(),
        ],
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TeamUpdateView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    @swagger_auto_schema(
        operation_description="Update a team by ID",
        request_body=TeamSerializer,
        responses={
            200: openapi.Response(
                description="Team updated successfully",
                schema=TeamSerializer,
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        manual_parameters=[
            get_authorization_parameter(),
        ],
        security=[{"Bearer": []}]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partial update a team by ID",
        request_body=TeamSerializer,
        responses={
            200: openapi.Response(
                description="Team updated successfully",
                schema=TeamSerializer,
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        manual_parameters=[
            get_authorization_parameter(),
        ],
        security=[{"Bearer": []}]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class TeamDeleteView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    @swagger_auto_schema(
        operation_description="Delete a team by ID",
        responses={204: "No Content", 404: "Not Found"},
        manual_parameters=[
            get_authorization_parameter(),
        ],
        security=[{"Bearer": []}]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
