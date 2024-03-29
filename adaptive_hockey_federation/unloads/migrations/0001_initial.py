# Generated by Django 4.2.10 on 2024-03-20 17:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Unload",
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
                    models.CharField(help_text="", max_length=256, verbose_name=""),
                ),
                (
                    "date",
                    models.DateField(auto_now_add=True, verbose_name="Дата выгрузки"),
                ),
                (
                    "file_slug",
                    models.FileField(upload_to="data/", verbose_name="Ссылка на файл"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Выгрузка",
                "verbose_name_plural": "Выгрузки",
                "ordering": ("date",),
            },
        ),
    ]
