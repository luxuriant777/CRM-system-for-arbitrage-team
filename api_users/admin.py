from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Permission


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "first_name", "last_name", "position"]


admin.site.register(Permission)
