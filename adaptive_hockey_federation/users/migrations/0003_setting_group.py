from django.db import migrations


def set_default_groups(apps, schema_editor):
    Group = apps.get_model("users", "ProxyGroup")
    Group.objects.bulk_create(
        [
            Group(name="Administrators"),
            Group(name="Moderators"),
            Group(name="Agents"),
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_proxygroup_alter_user_email"),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
    ]
