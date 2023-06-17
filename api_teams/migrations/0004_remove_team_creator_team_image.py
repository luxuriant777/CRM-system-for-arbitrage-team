# Generated by Django 4.2.1 on 2023-06-17 13:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_teams", "0003_team_creator"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="creator",
        ),
        migrations.AddField(
            model_name="team",
            name="image",
            field=models.ImageField(
                blank=True,
                default="team_images/default.jpg",
                null=True,
                upload_to="team_images",
            ),
        ),
    ]
