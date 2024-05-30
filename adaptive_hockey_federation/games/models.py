from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from competitions.models import Competition
from core.constants import NAME_MAX_LENGTH
from core.validators import validate_game_date
from games.constants import NumericalValues
from main.models import Player, Team


class Game(models.Model):
    """Модель игры."""

    name = models.CharField(
        verbose_name=_("Название игры"),
        max_length=NAME_MAX_LENGTH,
    )
    date = models.DateTimeField(
        verbose_name=_("Дата игры"),
        validators=[validate_game_date],  # type: ignore[list-item]
    )
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        verbose_name=_("Соревнование"),
        related_name="games",
    )
    game_teams = models.ManyToManyField(
        Team,
        verbose_name=_("Команды"),
        related_name="game_teams",
    )
    video_link = models.URLField(verbose_name=_("Ссылка на видео"), blank=True)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(date__lte=Now()),
                name="game_date_must_not_be_in_the_future",
            ),
        ]

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class GameTeam(models.Model):
    """Модель команды, участвующей в игре."""

    name = models.CharField(
        verbose_name=_("Название команды"),
        max_length=NAME_MAX_LENGTH,
    )
    discipline_name = models.CharField(
        verbose_name=_("Дисциплина"),
        max_length=NAME_MAX_LENGTH,
    )
    game_players = models.ManyToManyField(
        Player,
        verbose_name=_("Игроки"),
        related_name="game_players",
    )

    class Meta:
        verbose_name = "Команда, участвующая в игре"
        verbose_name_plural = "Команды, участвующие в игре"
        ordering = ["name"]

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class GamePlayer(models.Model):
    """Модель игрока, участвующего в игре."""

    name = models.CharField(
        verbose_name=_("Игрок"),
        max_length=NAME_MAX_LENGTH,
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_("Номер игрока"),
        validators=[
            MinValueValidator(
                NumericalValues.MIN_PLAYER_NUMBER,
                _("Номер игрока должен быть больше или равен нулю"),
            ),
            MaxValueValidator(
                NumericalValues.MAX_PLAYER_NUMBER,
                _("Номер игрока должен быть меньше или равен 99"),
            ),
        ],
    )
    game_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name=_("Команда"),
        related_name="game_team",
    )

    class Meta:
        unique_together = ("name", "number")
        verbose_name = "Игрок, участвующий в игре"
        verbose_name_plural = "Игроки, участвующие в игре"
        constraints = [
            models.CheckConstraint(
                check=models.Q(number__gte=NumericalValues.MIN_PLAYER_NUMBER),
                name="player_number_must_be_positive",
            ),
            models.CheckConstraint(
                check=models.Q(number__lte=NumericalValues.MAX_PLAYER_NUMBER),
                name=f"player_number_must_"
                f"be_{NumericalValues.MAX_PLAYER_NUMBER}_or_less",
            ),
        ]

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name
