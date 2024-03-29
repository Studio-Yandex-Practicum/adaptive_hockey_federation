# Generated by Django 4.2.8 on 2023-12-30 06:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_staffmember_staff_member_unique_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='curator',
            field=models.ForeignKey(help_text='Куратор команды', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Куратор команды'),
        ),
        migrations.AlterField(
            model_name='team',
            name='staff_team_member',
            field=models.ForeignKey(help_text='Сотрудник команды', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.staffteammember', verbose_name='Сотрудник команды'),
        ),
    ]
