from drf_yasg.utils import swagger_auto_schema
from crm_arbitrage.utils import get_authorization_parameter
from .tasks import process_lead
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Lead
from .serializers import LeadSerializer


class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer

    def perform_create(self, serializer):
        lead_data = serializer.validated_data
        process_lead.delay(lead_data)


class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all users",
        responses={
            200: LeadSerializer(many=True),
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
