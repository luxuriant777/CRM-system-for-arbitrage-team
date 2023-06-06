from django.urls import path
from .views import LeadCreateView, LeadListView, OrderCreateView, OrderListView

app_name = "customer_management"

urlpatterns = [
    path("leads/create/", LeadCreateView.as_view(), name="lead-create"),
    path("leads/list/", LeadListView.as_view(), name="lead-list"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/list/", OrderListView.as_view(), name="order-list"),
]
