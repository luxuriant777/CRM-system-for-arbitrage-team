from rest_framework import serializers

from api_users.models import Position
from api_users.serializers import CustomUserSerializer
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    members = CustomUserSerializer(many=True, read_only=True)
    creator = serializers.ReadOnlyField(source="creator.id")

    class Meta:
        model = Team
        fields = ["id", "name", "team_lead", "members", "creator"]

    def save(self, **kwargs):
        members = self.validated_data.pop("members", [])
        team = super().save(**kwargs)
        for member in members:
            if member.position != Position.BUYER or member.team_member.count() > 1:
                raise serializers.ValidationError("A buyer can only be a member of one team.")
            team.members.add(member)
        return team
