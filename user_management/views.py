from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRegistrationView(APIView):
    @staticmethod
    def post(request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserRegistrationSerializer(user)  # Serialize the user object
            return Response({'message': 'User registered successfully.', 'user': user_serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    @staticmethod
    def post(request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)

                payload = {
                    'user_id': user.id,
                    'username': user.username
                }

                access_token = refresh.access_token
                access_token['payload'] = payload

                return Response({'message': 'User logged in successfully.', 'access_token': str(access_token)},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
