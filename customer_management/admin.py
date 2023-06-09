from django.contrib import admin
from .models import Lead, Order


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["id", "ip_address", "user_agent", "referral_source", "created_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "lead_id",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "delivery_address",
        "created_at",
    ]
