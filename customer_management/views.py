from .tasks import process_lead, process_order
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Lead, Order
from .serializers import LeadSerializer, OrderSerializer, OrderListSerializer


class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer

    def perform_create(self, serializer):
        lead_data = serializer.validated_data
        process_lead.delay(lead_data)


class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order_data = serializer.validated_data
        process_order.delay(order_data)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
