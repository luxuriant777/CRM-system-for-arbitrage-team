from drf_yasg.utils import swagger_auto_schema
from crm_arbitrage.utils import get_authorization_parameter
from .tasks import process_prospect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Prospect
from .serializers import ProspectSerializer


class ProspectCreateView(generics.CreateAPIView):
    serializer_class = ProspectSerializer

    def perform_create(self, serializer):
        prospect_data = serializer.validated_data
        process_prospect.delay(prospect_data)


class ProspectListView(generics.ListAPIView):
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all prospects",
        responses={
            200: ProspectSerializer(many=True),
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
