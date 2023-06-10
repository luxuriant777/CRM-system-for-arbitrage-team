from rest_framework import serializers
from api_users.serializers import CustomUserSerializer
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    members = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "team_lead", "members"]
