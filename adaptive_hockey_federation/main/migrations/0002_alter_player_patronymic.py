# Generated by Django 4.2.7 on 2023-12-06 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='patronymic',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='Отчество'),
        ),
    ]
