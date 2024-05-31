# Generated by Django 4.2.8 on 2023-12-21 17:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0003_remove_player_player_position_number_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="curator",
            field=models.ForeignKey(
                default=0,
                help_text="Куратор команды",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Куратор команды",
            ),
            preserve_default=False,
        ),
    ]
