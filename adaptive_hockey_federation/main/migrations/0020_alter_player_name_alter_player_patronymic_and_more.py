# Generated by Django 4.2.10 on 2024-03-24 14:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0019_alter_staffmember_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="name",
            field=models.CharField(
                default="",
                help_text="Имя",
                max_length=256,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[А-Яа-яёA-Za-z -]+$",
                        "Строка должны состоять из кирилических или латинских символов.Возможно использование дефиса.",
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
                        "^[А-Яа-яёA-Za-z -]+$",
                        "Строка должны состоять из кирилических или латинских символов.Возможно использование дефиса.",
                    )
                ],
                verbose_name="Отчество",
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
                        "^[А-Яа-яёA-Za-z -]+$",
                        "Строка должны состоять из кирилических или латинских символов.Возможно использование дефиса.",
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
                        "^[А-Яа-яёA-Za-z -]+$",
                        "Строка должны состоять из кирилических или латинских символов.Возможно использование дефиса.",
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
                        "^[А-Яа-яёA-Za-z -]+$",
                        "Строка должны состоять из кирилических или латинских символов.Возможно использование дефиса.",
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
                        "^[А-Яа-яёA-Za-z -]+$",
                        "Строка должны состоять из кирилических или латинских символов.Возможно использование дефиса.",
                    )
                ],
                verbose_name="Фамилия",
            ),
        ),
    ]
