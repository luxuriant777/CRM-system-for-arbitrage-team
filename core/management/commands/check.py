from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = "Check for necessary permissions and create them if they do not exist."

    def handle(self, *args, **options):
        necessary_permissions = ["view_team_lead", "add_team_lead", "change_team_lead", "delete_team_lead",
                                 "view_buyer", "add_buyer", "change_buyer", "delete_buyer"]

        for perm_codename in necessary_permissions:
            if not Permission.objects.filter(codename=perm_codename).exists():
                # If not, call the "create_permissions" command.
                self.stdout.write(self.style.WARNING("Some necessary permissions are missing. Creating them now..."))
                management.call_command("create_permissions")
                break  # After calling "create_permissions", there is no need to continue checking permissions.
