from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth.models import Permission, Group
from api_users.models import Position


class Command(BaseCommand):
    help = "Check for necessary permissions and create them if they do not exist."

    def handle(self, *args, **options):
        necessary_permissions = ["view_team_lead", "add_team_lead", "change_team_lead", "delete_team_lead",
                                 "view_buyer", "add_buyer", "change_buyer", "delete_buyer"]

        necessary_groups = [Position.BUYER, Position.TEAM_LEAD, Position.OWNER]

        permissions_exist = all(Permission.objects.filter(codename=perm_codename).exists()
                                for perm_codename in necessary_permissions)

        groups_exist = all(Group.objects.filter(name=group_name).exists()
                           for group_name in necessary_groups)

        if not permissions_exist:
            # If necessary permissions do not exist, call the "create_permissions" command.
            self.stdout.write(self.style.WARNING("Some necessary permissions are missing. Creating them now..."))
            management.call_command("create_permissions")

        if not groups_exist:
            # If necessary groups do not exist, call the "create_groups" command.
            self.stdout.write(self.style.WARNING("Some necessary groups are missing. Creating them now..."))
            management.call_command("create_groups")
