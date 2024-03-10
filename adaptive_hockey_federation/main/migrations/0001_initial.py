# Generated by Django 4.2.11 on 2024-03-10 00:54

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Наименование",
                        max_length=256,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
            ],
            options={
                "verbose_name": "Город",
                "verbose_name_plural": "Города",
            },
        ),
        migrations.CreateModel(
            name="Diagnosis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Наименование",
                        max_length=256,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
            ],
            options={
                "verbose_name": "Диагноз",
                "verbose_name_plural": "Диагнозы",
            },
        ),
        migrations.CreateModel(
            name="Discipline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Дисциплина",
                "verbose_name_plural": "Дисциплины",
            },
        ),
        migrations.CreateModel(
            name="DisciplineLevel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Наименование",
                        max_length=256,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
            ],
            options={
                "verbose_name": "Классификация/статус дисциплины",
                "verbose_name_plural": "Классификация/статусы дисциплин",
            },
        ),
        migrations.CreateModel(
            name="DisciplineName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Наименование",
                        max_length=256,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
            ],
            options={
                "verbose_name": "Название дисциплины",
                "verbose_name_plural": "Названия дисциплин",
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Наименование",
                        max_length=256,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        max_length=256,
                        unique=True,
                        upload_to="documents"
                    ),
                ),
            ],
            options={
                "verbose_name": "Документ",
                "verbose_name_plural": "Документы",
            },
        ),
        migrations.CreateModel(
            name="Nosology",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Наименование",
                        max_length=256,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
            ],
            options={
                "verbose_name": "Нозология",
                "verbose_name_plural": "Нозология",
            },
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        default="",
                        help_text="Фамилия",
                        max_length=256,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="",
                        help_text="Имя",
                        max_length=256,
                        verbose_name="Имя"
                    ),
                ),
                (
                    "patronymic",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Отчество",
                        max_length=256,
                        verbose_name="Отчество",
                    ),
                ),
                (
                    "birthday",
                    models.DateField(
                        help_text="Дата рождения", verbose_name="Дата рождения"
                    ),
                ),
                (
                    "addition_date",
                    models.DateField(
                        default=django.utils.timezone.now,
                        help_text="Дата добавления в базу данных",
                        verbose_name="Дата добавления",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Мужской"),
                                 ("female", "Женский")],
                        default="",
                        help_text="Пол",
                        max_length=256,
                        verbose_name="Пол",
                    ),
                ),
                (
                    "level_revision",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Уровень ревизии",
                        verbose_name="Уровень ревизии",
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("striker", "Нападающий"),
                            ("bobber", "Поплавок"),
                            ("goalkeeper", "Вратарь"),
                            ("defender", "Защитник"),
                        ],
                        default="",
                        help_text="Игровая позиция",
                        max_length=256,
                        verbose_name="Игровая позиция",
                    ),
                ),
                (
                    "number",
                    models.IntegerField(
                        default=0,
                        help_text="Номер игрока",
                        verbose_name="Номер игрока"
                    ),
                ),
                (
                    "is_captain",
                    models.BooleanField(
                        default=False,
                        verbose_name="Капитан"
                    ),
                ),
                (
                    "is_assistent",
                    models.BooleanField(
                        default=False,
                        verbose_name="Ассистент"
                    ),
                ),
                (
                    "identity_document",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Удостоверение личности",
                        verbose_name="Удостоверение личности",
                    ),
                ),
            ],
            options={
                "verbose_name": "Игрок",
                "verbose_name_plural": "Игроки",
                "ordering": ("surname", "name", "patronymic"),
                "permissions": [("list_view_player",
                                 "Может видеть список игроков")],
                "abstract": False,
                "default_related_name": "players",
            },
        ),
        migrations.CreateModel(
            name="StaffMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        default="",
                        help_text="Фамилия",
                        max_length=256,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="",
                        help_text="Имя",
                        max_length=256,
                        verbose_name="Имя"
                    ),
                ),
                (
                    "patronymic",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Отчество",
                        max_length=256,
                        verbose_name="Отчество",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Номер телефона",
                        max_length=256,
                        verbose_name="Номер телефона",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сотрудник",
                "verbose_name_plural": "Сотрудники",
            },
        ),
        migrations.CreateModel(
            name="StaffTeamMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "staff_position",
                    models.CharField(
                        choices=[("trainer", "тренер"),
                                 ("other", "пушер-тьютор")],
                        default="",
                        help_text="Статус сотрудника",
                        max_length=256,
                        verbose_name="Статус сотрудника",
                    ),
                ),
                (
                    "qualification",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Квалификация",
                        max_length=256,
                        verbose_name="Квалификация",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Описание",
                        verbose_name="Описание",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сотрудник команды",
                "verbose_name_plural": "Сотрудники команды",
            },
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Наименование",
                        max_length=256,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        help_text="Город откуда команда",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.city",
                        verbose_name="Город откуда команда",
                    ),
                ),
            ],
            options={
                "verbose_name": "Команда",
                "verbose_name_plural": "Команды",
                "permissions": [("list_view_team",
                                 "Может видеть список команд")],
                "default_related_name": "teams",
            },
        ),
    ]
