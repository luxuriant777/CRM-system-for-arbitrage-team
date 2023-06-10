from django.db import models
from api_users.models import CustomUser, Position


class Team(models.Model):
    name = models.CharField(max_length=100)
    team_lead = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'position': Position.TEAM_LEAD},
        related_name="teams_lead",
    )
    members = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'position': Position.BUYER},
        related_name="teams_member",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
