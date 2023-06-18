from django.urls import path
from .views import OrderCreateView, OrderListView

app_name = "api_orders"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("list/", OrderListView.as_view(), name="order-list"),
]
