from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from user_management.models import CustomUser


class Command(BaseCommand):
    help = "Create permissions for custom user roles"

    def handle(self, *args, **options):        
        content_type = ContentType.objects.get_for_model(CustomUser)
        
        Permission.objects.create(
            codename="view_team_lead",
            name="Can view Team Lead",
            content_type=content_type,
        )
        Permission.objects.create(
            codename="add_team_lead",
            name="Can add Team Lead",
            content_type=content_type,
        )
        Permission.objects.create(
            codename="change_team_lead",
            name="Can change Team Lead",
            content_type=content_type,
        )
        Permission.objects.create(
            codename="delete_team_lead",
            name="Can delete Team Lead",
            content_type=content_type,
        )
        
        Permission.objects.create(
            codename="view_buyer",
            name="Can view Buyer",
            content_type=content_type,
        )
        Permission.objects.create(
            codename="add_buyer",
            name="Can add Buyer",
            content_type=content_type,
        )
        Permission.objects.create(
            codename="change_buyer",
            name="Can change Buyer",
            content_type=content_type,
        )
        Permission.objects.create(
            codename="delete_buyer",
            name="Can delete Buyer",
            content_type=content_type,
        )
