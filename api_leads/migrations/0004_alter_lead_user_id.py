# Generated by Django 4.2.1 on 2023-06-10 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_leads", "0003_remove_lead_user_lead_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lead",
            name="user_id",
            field=models.IntegerField(default=1),
        ),
    ]
