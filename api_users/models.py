from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.TextChoices):
    BUYER = "Buyer", "Buyer"
    TEAM_LEAD = "Team Lead", "Team Lead"
    FUNDS_COORDINATOR = "Funds Coordinator", "Funds Coordinator"
    OWNER = "Owner", "Owner"


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.BUYER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="user_images", default="user_images/default.jpg", null=True, blank=True)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username
