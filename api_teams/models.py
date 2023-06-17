from django.db import models
from api_users.models import CustomUser, Position


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
    image = models.ImageField(upload_to="team_images", default="team_images/default.jpg", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
