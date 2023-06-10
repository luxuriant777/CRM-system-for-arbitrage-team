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
