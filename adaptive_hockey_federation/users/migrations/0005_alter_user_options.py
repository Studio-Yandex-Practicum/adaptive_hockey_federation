# Generated by Django 4.2.10 on 2024-03-11 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('last_name',), 'permissions': [('list_view_user', 'Can view list of Пользователь')], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
