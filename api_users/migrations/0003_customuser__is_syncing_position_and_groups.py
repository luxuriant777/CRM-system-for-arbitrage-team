# Generated by Django 4.2.1 on 2023-06-11 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_users", "0002_alter_customuser_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="_is_syncing_position_and_groups",
            field=models.BooleanField(default=False, editable=False),
        ),
    ]