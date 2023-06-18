from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from api_users.models import Position


class Command(BaseCommand):
    help = "Create groups and assign permissions based on user roles"

    def handle(self, *args, **options):
        buyer_permissions = [
            "view_prospect", 
            "view_order", 
            "view_team"
        ]
        
        team_lead_permissions = [
            "view_prospect", 
            "add_prospect",
            "change_prospect",
            "delete_prospect",
            "view_order", 
            "add_order", 
            "change_order", 
            "delete_order", 
            "view_team", 
            "add_team", 
            "change_team", 
            "delete_team"
        ]

        owner_permissions = Permission.objects.all().values_list("codename", flat=True)

        groups = {
            Position.BUYER: buyer_permissions,
            Position.TEAM_LEAD: team_lead_permissions,
            Position.OWNER: owner_permissions
        }

        for group_name, permission_codenames in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)

            for codename in permission_codenames:
                permission = Permission.objects.get(codename=codename)
                if not group.permissions.filter(id=permission.id).exists():
                    group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS("Groups are created successfully."))
