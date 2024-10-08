from core.constants import GROUPS_BY_ROLE
from django.contrib.auth.management import create_permissions
from django.db import migrations
from users.constants import GroupPermission


def set_default_groups(apps, schema_editor):
    Group = apps.get_model("users", "ProxyGroup")
    Group.objects.bulk_create(
        [Group(name=name) for name in set(GROUPS_BY_ROLE.values())]
    )


def set_permissions_to_groups(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        del app_config.models_module

    Group = apps.get_model("users", "ProxyGroup")
    Permission = apps.get_model("auth", "Permission")

    for group in Group.objects.all():
        if GroupPermission.GROUP_PERMISSION[group.name][0] == "include":
            for codename in GroupPermission.GROUP_PERMISSION[group.name][1]:
                group.permissions.add(Permission.objects.get(codename=codename))
            continue
        for perm in Permission.objects.all():
            if perm.codename not in GroupPermission.GROUP_PERMISSION[group.name][1]:
                group.permissions.add(perm)
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
        migrations.RunPython(
            set_permissions_to_groups,
        ),
    ]
