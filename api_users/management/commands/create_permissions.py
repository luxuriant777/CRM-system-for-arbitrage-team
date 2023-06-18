from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from api_users.models import CustomUser


class Command(BaseCommand):
    help = "Create permissions for custom user roles"

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(CustomUser)

        permissions = [
            {"codename": "view_team_lead", "name": "Can view Team Prospect"},
            {"codename": "add_team_lead", "name": "Can add Team Prospect"},
            {"codename": "change_team_lead", "name": "Can change Team Prospect"},
            {"codename": "delete_team_lead", "name": "Can delete Team Prospect"},
            {"codename": "view_buyer", "name": "Can view Buyer"},
            {"codename": "add_buyer", "name": "Can add Buyer"},
            {"codename": "change_buyer", "name": "Can change Buyer"},
            {"codename": "delete_buyer", "name": "Can delete Buyer"},
        ]

        for perm in permissions:
            Permission.objects.get_or_create(codename=perm["codename"], defaults={
                "name": perm["name"],
                "content_type": content_type,
            })

        self.stdout.write(self.style.SUCCESS("Custom permissions are created successfully."))
