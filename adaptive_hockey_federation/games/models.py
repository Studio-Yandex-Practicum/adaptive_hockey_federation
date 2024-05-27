from competitions.models import Competition
from core.constants import (
    MAX_PLAYER_NUMBER,
    MIN_PLAYER_NUMBER,
    NAME_MAX_LENGTH,
)
from core.validators import validate_game_date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _
from main.models import Team


class Game(models.Model):
    """Модель игры."""

    name = models.CharField(
        verbose_name=_("Название игры"), max_length=NAME_MAX_LENGTH
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
        related_name="teams",
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
        return self.name


class GameTeam(models.Model):
    """Модель команды, участвующей в игре."""

    name = models.CharField(
        verbose_name=_("Название команды"),
        help_text=_("Название команды"),
        max_length=NAME_MAX_LENGTH,
    )
    discipline_name = models.CharField(
        verbose_name=_("Дисциплина"),
        help_text=_("Дисциплина"),
        max_length=NAME_MAX_LENGTH,
    )
    game_players = models.ManyToManyField(
        Team,
        verbose_name=_("Игроки"),
        help_text=_("Игроки, участвующие в игре"),
        related_name="players",
    )

    class Meta:
        verbose_name = "Команда в игре"
        verbose_name_plural = "Команды в игре"
        ordering = ["name"]

    def __str__(self):
        return self.name


class GamePlayer(models.Model):
    """Модель игрока, участвующего в игре."""

    name = models.CharField(
        verbose_name=_("Игрок"), max_length=NAME_MAX_LENGTH
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_("Номер игрока"),
        help_text=_("Номер игрока"),
        validators=[
            MinValueValidator(
                MIN_PLAYER_NUMBER,
                _("Номер игрока должен быть больше или равен нулю"),
            ),
            MaxValueValidator(
                MAX_PLAYER_NUMBER,
                _("Номер игрока должен быть меньше или равен 99"),
            ),
        ],
    )
    game_team = models.CharField(
        verbose_name=_("Команда"),
        help_text=_("Команда"),
        max_length=NAME_MAX_LENGTH,
    )

    class Meta:
        unique_together = ("name", "number")
        verbose_name = "Игрок в игре"
        verbose_name_plural = "Игроки в игре"
        constraints = [
            models.CheckConstraint(
                check=models.Q(number__gte=MIN_PLAYER_NUMBER),
                name="player_number_must_be_positive",
            ),
            models.CheckConstraint(
                check=models.Q(number__lte=MAX_PLAYER_NUMBER),
                name=f"player_number_be_{MAX_PLAYER_NUMBER}_or_less",
            ),
        ]

    def __str__(self):
        return self.name
