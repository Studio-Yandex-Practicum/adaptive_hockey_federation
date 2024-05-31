# Generated by Django 4.2.10 on 2024-03-11 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0016_alter_staffteammember_staff_position"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="player",
            options={
                "default_related_name": "players",
                "ordering": ("surname", "name", "patronymic"),
                "permissions": [("list_view_player", "Can view list of Игрок")],
                "verbose_name": "Игрок",
                "verbose_name_plural": "Игроки",
            },
        ),
        migrations.AlterModelOptions(
            name="team",
            options={
                "default_related_name": "teams",
                "permissions": [("list_view_team", "Can view list of Команда")],
                "verbose_name": "Команда",
                "verbose_name_plural": "Команды",
            },
        ),
    ]
