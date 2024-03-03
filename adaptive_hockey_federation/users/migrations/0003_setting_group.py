from django.contrib.auth.management import create_permissions
from django.db import migrations
from users.constants import GROUP_PERMISSION


def set_default_groups(apps, schema_editor):
    Group = apps.get_model("users", "ProxyGroup")
    Group.objects.bulk_create(
        [
            Group(name="Администраторы"),
            Group(name="Модераторы"),
            Group(name="Представители команд"),
        ]
    )


def set_permissions_to_groups(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        del app_config.models_module
    Group = apps.get_model("users", "ProxyGroup")
    Permission = apps.get_model("auth", "Permission")
    for group in Group.objects.all():
        if not GROUP_PERMISSION[group.name]:
            for perm in Permission.objects.all():
                group.permissions.add(perm)
            continue
        for codename in GROUP_PERMISSION[group.name]:
            group.permissions.add(
                Permission.objects.get(codename=codename)
            )
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_proxygroup_alter_user_email"),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
        migrations.RunPython(
            set_permissions_to_groups,
        ),
    ]
