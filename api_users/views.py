from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from crm_arbitrage.utils import get_authorization_parameter
from .models import CustomUser
from .serializers import CustomUserRegistrationSerializer, CustomUserLoginSerializer, CustomUserSerializer


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all users",
        responses={
            200: CustomUserSerializer(many=True),
            401: "Unauthorized",
            500: "Internal Server Error"
        },
        manual_parameters=[
            get_authorization_parameter(),
        ],
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserRegistrationView(APIView):
    @swagger_auto_schema(
        operation_description="User Registration",
        request_body=CustomUserRegistrationSerializer,
        responses={
            201: "User registered successfully",
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = CustomUserRegistrationSerializer(
                user
            )
            return Response(
                {
                    "message": "User registered successfully.",
                    "user": user_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            errors = serializer.errors
            return Response(
                {"message": "Bad Request.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginView(APIView):
    @swagger_auto_schema(
        operation_description="User Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
            },
        ),
        responses={
            200: "OK",
            400: "Bad Request",
            401: "Unauthorized"
        }
    )
    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                payload = {"user_id": user.id, "username": user.username}
                access_token = refresh.access_token
                access_token["payload"] = payload

                return Response(
                    {
                        "message": "User logged in successfully.",
                        "access_token": str(access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            errors = serializer.errors
            return Response(
                {"message": "Bad Request.", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
