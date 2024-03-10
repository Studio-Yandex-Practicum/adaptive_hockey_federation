# Generated by Django 4.2.11 on 2024-03-10 00:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "main", "0001_initial"
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="curator",
            field=models.ForeignKey(
                help_text="Куратор команды",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="team",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Куратор команды",
            ),
        ),
        migrations.AddField(
            model_name="team",
            name="discipline_name",
            field=models.ForeignKey(
                help_text="Дисциплина команды",
                on_delete=django.db.models.deletion.CASCADE,
                to="main.disciplinename",
                verbose_name="Дисциплина команды",
            ),
        ),
        migrations.AddField(
            model_name="staffteammember",
            name="staff_member",
            field=models.ForeignKey(
                help_text="Сотрудник",
                on_delete=django.db.models.deletion.CASCADE,
                to="main.staffmember",
                verbose_name="Сотрудник",
            ),
        ),
        migrations.AddField(
            model_name="staffteammember",
            name="team",
            field=models.ManyToManyField(
                help_text="Команда",
                related_name="team_members",
                to="main.team",
                verbose_name="Команда",
            ),
        ),
        migrations.AddConstraint(
            model_name="staffmember",
            constraint=models.UniqueConstraint(
                fields=(
                    "name",
                    "surname",
                    "patronymic"
                ),
                name="staff_member_unique"
            ),
        ),
        migrations.AddField(
            model_name="player",
            name="diagnosis",
            field=models.ForeignKey(
                help_text="Диагноз",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="player_diagnosis",
                to="main.diagnosis",
                verbose_name="Диагноз",
            ),
        ),
        migrations.AddField(
            model_name="player",
            name="discipline",
            field=models.ForeignKey(
                help_text="Дисциплина",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="player_disciplines",
                to="main.discipline",
                verbose_name="Дисциплина",
            ),
        ),
        migrations.AddField(
            model_name="player",
            name="team",
            field=models.ManyToManyField(
                help_text="Команда",
                related_name="team_players",
                to="main.team",
                verbose_name="Команда",
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="player",
            field=models.ForeignKey(
                blank=True,
                default="",
                help_text="Игрок",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="player_documemts",
                to="main.player",
                verbose_name="Игрок",
            ),
        ),
        migrations.AddField(
            model_name="discipline",
            name="discipline_level",
            field=models.ForeignKey(
                help_text="Класс/статус",
                max_length=10,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="disciplines",
                to="main.disciplinelevel",
                verbose_name="Класс/статус",
            ),
        ),
        migrations.AddField(
            model_name="discipline",
            name="discipline_name",
            field=models.ForeignKey(
                help_text="Название дисциплины",
                max_length=10,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="disciplines",
                to="main.disciplinename",
                verbose_name="Название дисциплины",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="nosology",
            field=models.ForeignKey(
                help_text="Нозология",
                max_length=10,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diagnosis",
                to="main.nosology",
                verbose_name="Нозология",
            ),
        ),
        migrations.AddConstraint(
            model_name="team",
            constraint=models.UniqueConstraint(
                fields=(
                    "name",
                    "city",
                    "discipline_name"
                ),
                name="team_city_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="staffteammember",
            constraint=models.UniqueConstraint(
                fields=(
                    "staff_member",
                    "staff_position"
                ),
                name="staff_member_position_unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="player",
            constraint=models.UniqueConstraint(
                fields=(
                    "name",
                    "surname",
                    "patronymic",
                    "birthday"
                ),
                name="player_unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="document",
            constraint=models.UniqueConstraint(
                fields=(
                    "file",
                    "player"
                ),
                name="player_docume_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="discipline",
            constraint=models.UniqueConstraint(
                fields=(
                    "discipline_name",
                    "discipline_level"
                ),
                name="discipline_name_level_unique",
            ),
        ),
    ]
