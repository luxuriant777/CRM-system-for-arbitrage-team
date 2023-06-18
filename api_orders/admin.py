from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "prospect_id",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "delivery_address",
        "created_at",
    ]
