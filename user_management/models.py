from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.TextChoices):
    BUYER = 'Buyer', 'Buyer'
    TEAM_LEAD = 'Team Lead', 'Team Lead'
    OWNER = 'Owner', 'Owner'


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.BUYER,
    )
    image = models.ImageField(upload_to="profile_images", default="profile_images/default.jpg")

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
