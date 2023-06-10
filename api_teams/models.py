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

    def save(self, *args, **kwargs):
        if self.members.filter(position=Position.BUYER).annotate(num_teams=Count('teams_member')).filter(num_teams__gt=1).exists():
            raise ValidationError("A buyer can only be a member of one team.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
