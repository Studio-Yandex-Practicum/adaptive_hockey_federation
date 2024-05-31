# Generated by Django 4.2.13 on 2024-05-31 06:49

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.datetime
import games.constants


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("main", "0001_initial"),
        ("competitions", "0002_initial"),
        ("games", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gameteam",
            name="game_players",
            field=models.ManyToManyField(
                related_name="game_players", to="main.player", verbose_name="Игроки"
            ),
        ),
        migrations.AddField(
            model_name="gameplayer",
            name="game_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="game_team",
                to="main.team",
                verbose_name="Команда",
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="competition",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="games",
                to="competitions.competition",
                verbose_name="Соревнование",
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="game_teams",
            field=models.ManyToManyField(
                related_name="game_teams", to="main.team", verbose_name="Команды"
            ),
        ),
        migrations.AddConstraint(
            model_name="gameplayer",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "number__gte",
                        games.constants.NumericalValues["GAME_MIN_PLAYER_NUMBER"],
                    )
                ),
                name="player_number_must_be_positive",
            ),
        ),
        migrations.AddConstraint(
            model_name="gameplayer",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "number__lte",
                        games.constants.NumericalValues["GAME_MAX_PLAYER_NUMBER"],
                    )
                ),
                name="player_number_must_be_99_or_less",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="gameplayer",
            unique_together={("name", "number")},
        ),
        migrations.AddConstraint(
            model_name="game",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("date__lte", django.db.models.functions.datetime.Now())
                ),
                name="game_date_must_not_be_in_the_future",
            ),
        ),
    ]
