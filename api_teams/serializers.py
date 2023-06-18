from rest_framework import serializers

from api_users.models import Position, CustomUser
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.filter(position=Position.BUYER),
                                                 required=False)

    class Meta:
        model = Team
        fields = ["id", "name", "team_lead", "members"]

    def validate_members(self, members):
        for member in members:
            if member.team_member.count() > 0:
                raise serializers.ValidationError(f"A Buyer with id {member.id} can only be a member of one team.")
        return members
