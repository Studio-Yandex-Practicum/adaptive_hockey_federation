# Generated by Django 4.2.8 on 2023-12-17 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_player_patronymic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='patronymic',
            field=models.CharField(blank=True, default='--пусто--', help_text='Отчество', max_length=256, verbose_name='Отчество'),
        ),
    ]
