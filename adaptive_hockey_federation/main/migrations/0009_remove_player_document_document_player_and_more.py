# Generated by Django 4.2.8 on 2024-01-29 05:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_team_curator_alter_team_staff_team_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='document',
        ),
        migrations.AddField(
            model_name='document',
            name='player',
            field=models.ForeignKey(blank=True, default='', help_text='Игрок', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_documemts', to='main.player', verbose_name='Игрок'),
        ),
        migrations.AlterField(
            model_name='player',
            name='is_assistent',
            field=models.BooleanField(default=False, verbose_name='Ассистент'),
        ),
        migrations.AlterField(
            model_name='player',
            name='is_captain',
            field=models.BooleanField(default=False, verbose_name='Капитан'),
        ),
    ]
