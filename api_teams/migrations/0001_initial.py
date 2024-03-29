# Generated by Django 4.2.1 on 2023-06-18 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="team_images/default.jpg",
                        null=True,
                        upload_to="team_images",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        blank=True,
                        limit_choices_to={"position": "Buyer"},
                        related_name="team_member",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team_lead",
                    models.OneToOneField(
                        limit_choices_to={"position": "Team Lead"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="team_lead",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]
