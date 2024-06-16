from competitions.models import Competition
from core.constants import UserConstans
from core.validators import validate_game_date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _
from games.constants import NumericalValues


class Game(models.Model):
    """Модель игры."""

    name = models.CharField(
        verbose_name=_("Название игры"),
        max_length=UserConstans.NAME_MAX_LENGTH,
    )
    date = models.DateTimeField(
        verbose_name=_("Дата игры"),
        validators=[
            validate_game_date,
        ],
    )
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        verbose_name=_("Соревнование"),
    )
    video_link = models.URLField(verbose_name=_("Ссылка на видео"), blank=True)

    class Meta:
        default_related_name = "games"
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ("name",)
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
    """
    Модель команды, участвующей в игре.

    В данной модели переопределено стандартное поле ID — оно заменено на
    IntegerField для синхронизации ID сущностей данной модели и модели Team.
    В качестве Primary Key выступает поле gameteam_id.
    """

    gameteam_id = models.BigAutoField(primary_key=True)
    id = models.IntegerField()
    name = models.CharField(
        verbose_name=_("Название команды"),
        max_length=UserConstans.NAME_MAX_LENGTH,
    )
    discipline_name = models.CharField(
        verbose_name=_("Дисциплина"),
        max_length=UserConstans.NAME_MAX_LENGTH,
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name=_("Игра"),
    )

    class Meta:
        default_related_name = "game_teams"
        verbose_name = "Команда, участвующая в игре"
        verbose_name_plural = "Команды, участвующие в игре"
        ordering = ("name",)

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class GamePlayer(models.Model):
    """
    Модель игрока, участвующего в игре.

    В данной модели переопределено стандартное поле ID — оно заменено на
    IntegerField для синхронизации ID сущностей данной модели и модели Player.
    В качестве Primary Key выступает поле gameplayer_id.
    """

    gameplayer_id = models.BigAutoField(primary_key=True)
    id = models.IntegerField()
    name = models.CharField(
        verbose_name=_("Имя игрока"),
        max_length=UserConstans.NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        verbose_name=_("Фамилия игрока"),
        max_length=UserConstans.NAME_MAX_LENGTH,
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_("Номер игрока"),
        validators=[
            MinValueValidator(
                NumericalValues.GAME_MIN_PLAYER_NUMBER,
                _("Номер игрока должен быть больше или равен нулю"),
            ),
            MaxValueValidator(
                NumericalValues.GAME_MAX_PLAYER_NUMBER,
                _("Номер игрока должен быть меньше или равен 99"),
            ),
        ],
    )
    game_team = models.ForeignKey(
        GameTeam,
        on_delete=models.CASCADE,
        verbose_name=_("Команда"),
    )

    class Meta:
        default_related_name = "game_players"
        unique_together = (
            "name",
            "number",
            "game_team",
        )
        verbose_name = "Игрок, участвующий в игре"
        verbose_name_plural = "Игроки, участвующие в игре"
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    number__gte=NumericalValues.GAME_MIN_PLAYER_NUMBER,
                ),
                name="player_number_must_be_positive",
            ),
            models.CheckConstraint(
                check=models.Q(
                    number__lte=NumericalValues.GAME_MAX_PLAYER_NUMBER,
                ),
                name=f"player_number_must_"
                f"be_{NumericalValues.GAME_MAX_PLAYER_NUMBER}_or_less",
            ),
        ]

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return f"{self.name} {self.last_name}"
