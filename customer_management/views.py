from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Lead, Order
from .serializers import LeadSerializer, OrderSerializer


class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer


class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
