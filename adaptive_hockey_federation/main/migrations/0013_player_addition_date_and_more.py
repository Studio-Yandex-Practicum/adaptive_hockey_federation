# Generated by Django 4.2.10 on 2024-02-23 16:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0012_alter_staffteammember_staff_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="addition_date",
            field=models.DateField(
                default=django.utils.timezone.now,
                help_text="Дата добавления в базу данных",
                verbose_name="Дата добавления",
            ),
        ),
        migrations.AlterField(
            model_name="staffteammember",
            name="staff_position",
            field=models.CharField(
                choices=[("trainer", "тренер"), ("other", "другой")],
                default="",
                help_text="Статус сотрудника",
                max_length=256,
                verbose_name="Статус сотрудника",
            ),
        ),
    ]
