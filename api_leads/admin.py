from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["id", "ip_address", "user_agent", "referral_source", "created_at"]
