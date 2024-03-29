# Generated by Django 4.2.10 on 2024-03-18 10:22

import core.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0017_alter_player_options_alter_team_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="birthday",
            field=models.DateField(
                help_text="Дата рождения",
                validators=[core.validators.validate_date_birth],
                verbose_name="Дата рождения",
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="gender",
            field=models.CharField(
                choices=[("Мужской", "Мужской"), ("Женский", "Женский")],
                default="",
                help_text="Пол",
                max_length=256,
                verbose_name="Пол",
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="name",
            field=models.CharField(
                default="",
                help_text="Имя",
                max_length=256,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[А-Яа-яё -]+$",
                        "Строка должны состоять из кирилических символов. Возможно использование дефиса.",
                    )
                ],
                verbose_name="Имя",
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="patronymic",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Отчество",
                max_length=256,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[А-Яа-яё -]+$",
                        "Строка должны состоять из кирилических символов. Возможно использование дефиса.",
                    )
                ],
                verbose_name="Отчество",
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="position",
            field=models.CharField(
                choices=[
                    ("Нападающий", "Нападающий"),
                    ("Поплавок", "Поплавок"),
                    ("Вратарь", "Вратарь"),
                    ("Защитник", "Защитник"),
                ],
                default="",
                help_text="Игровая позиция",
                max_length=256,
                verbose_name="Игровая позиция",
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="surname",
            field=models.CharField(
                default="",
                help_text="Фамилия",
                max_length=256,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[А-Яа-яё -]+$",
                        "Строка должны состоять из кирилических символов. Возможно использование дефиса.",
                    )
                ],
                verbose_name="Фамилия",
            ),
        ),
        migrations.AlterField(
            model_name="staffmember",
            name="name",
            field=models.CharField(
                default="",
                help_text="Имя",
                max_length=256,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[А-Яа-яё -]+$",
                        "Строка должны состоять из кирилических символов. Возможно использование дефиса.",
                    )
                ],
                verbose_name="Имя",
            ),
        ),
        migrations.AlterField(
            model_name="staffmember",
            name="patronymic",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Отчество",
                max_length=256,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[А-Яа-яё -]+$",
                        "Строка должны состоять из кирилических символов. Возможно использование дефиса.",
                    )
                ],
                verbose_name="Отчество",
            ),
        ),
        migrations.AlterField(
            model_name="staffmember",
            name="surname",
            field=models.CharField(
                default="",
                help_text="Фамилия",
                max_length=256,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[А-Яа-яё -]+$",
                        "Строка должны состоять из кирилических символов. Возможно использование дефиса.",
                    )
                ],
                verbose_name="Фамилия",
            ),
        ),
        migrations.AlterField(
            model_name="staffteammember",
            name="staff_position",
            field=models.CharField(
                choices=[("тренер", "тренер"), ("пушер-тьютор", "пушер-тьютор")],
                default="",
                help_text="Статус сотрудника",
                max_length=256,
                verbose_name="Статус сотрудника",
            ),
        ),
    ]
