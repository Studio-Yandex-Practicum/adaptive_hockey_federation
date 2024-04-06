# Generated by Django 4.2.10 on 2024-04-06 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("unloads", "0004_alter_unload_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unload",
            name="unload_file_slug",
            field=models.FileField(
                upload_to="unloads_data/", verbose_name="Ссылка на файл"
            ),
        ),
    ]
