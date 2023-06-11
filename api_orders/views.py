from drf_yasg.utils import swagger_auto_schema

from crm_arbitrage.utils import get_authorization_parameter
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

    @swagger_auto_schema(
        operation_description="List all users",
        responses={
            200: OrderListSerializer(many=True),
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
