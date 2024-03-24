# Generated by Django 4.2.10 on 2024-03-24 14:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
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
            model_name="user",
            name="last_name",
            field=models.CharField(
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
            model_name="user",
            name="patronymic",
            field=models.CharField(
                blank=True,
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
    ]