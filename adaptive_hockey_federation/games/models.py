from core.constants import NAME_MAX_LENGTH
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import Team


class Game(models.Model):
    """Модель игры."""

    name = models.CharField(_("Название игры"), max_length=NAME_MAX_LENGTH)
    video_link = models.URLField(_("Ссылка на видео"))
    teams = models.ManyToManyField(  # type:ignore
        Team,
        through="GameTeam",
        through_fields=("game", "team"),
        verbose_name=_("Команды"),
        help_text=_("Команды участвующие в игре"),
    )

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class GameTeam(models.Model):
    """Промежуточная модель, связь с командой "Многие ко многим"."""

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="game_teams",
        verbose_name=_("Игра"),
        help_text=_("Игра, в которой участвует команда"),
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="game_teams",
        verbose_name=_("Команда"),
        help_text=_("Команда, участвующая в игре"),
    )
    is_away = models.BooleanField(_("Выездная команда"), default=False)

    class Meta:
        unique_together = ("game", "team")
        verbose_name = "Команда в игре"
        verbose_name_plural = "Команды в играх"

    def __str__(self):
        return f"{self.game} - {self.team}"
