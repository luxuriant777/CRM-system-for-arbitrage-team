from django.db import models
from django.db.models import Count
from api_users.models import CustomUser, Position
from django.core.exceptions import ValidationError


class Team(models.Model):
    name = models.CharField(max_length=100)
    team_lead = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"position": Position.TEAM_LEAD},
        related_name="team_lead",
    )
    members = models.ManyToManyField(
        CustomUser,
        limit_choices_to={"position": Position.BUYER},
        related_name="team_member",
        blank=True,
    )
    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="team_creator"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
