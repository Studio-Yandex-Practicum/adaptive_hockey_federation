def set_default_permission_group(sender, **kwargs):
    from django.contrib.auth.models import Permission
    from users.constants import AGENTS_PERMS, GROUP_NAMES, MODERATORS_PERMS
    from users.models import ProxyGroup
    for group in GROUP_NAMES:
        group_obj = ProxyGroup.objects.get(name=group)
        if group == "Administrators":
            for perm in Permission.objects.all():
                group_obj.permissions.add(perm)
        elif group == "Moderators":
            for codename in MODERATORS_PERMS:
                group_obj.permissions.add(Permission.objects.get(
                    codename=codename))
        elif group == "Agents":
            for codename in AGENTS_PERMS:
                group_obj.permissions.add(Permission.objects.get(
                    codename=codename))
