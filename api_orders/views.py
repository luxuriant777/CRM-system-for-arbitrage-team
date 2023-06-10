from .tasks import process_order
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer, OrderListSerializer


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order_data = serializer.validated_data
        process_order.delay(order_data)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
