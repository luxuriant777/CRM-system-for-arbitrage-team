from django.contrib import admin
from .models import Prospect


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = ["id", "ip_address", "user_agent", "referral_source", "created_at"]
