from competitions.utils import get_now_day, pluralize_days
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import City, Team

CHAR_FIELD_LENGTH = 250


class Competition(models.Model):
    """
    Модель соревнований.
    """

    title = models.CharField(max_length=CHAR_FIELD_LENGTH)
    date_start = models.DateField()
    date_end = models.DateField()
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name=_("Город проведения соревнований"),
        help_text=_("Город проведения соревнований"),
    )
    location = models.CharField(max_length=CHAR_FIELD_LENGTH)
    teams = models.ManyToManyField(
        Team,
        related_name="competition_teams",
        verbose_name=_("Состав команд участников"),
        help_text=_("Состав команд участников"),
    )

    class Meta:
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"
        ordering = ("date_start",)
        permissions = [
            ("list_view_competition", "Can view list of Соревнование"),
            (
                "list_team_competition",
                "Can view list of Команда on Соревнование",
            ),
            (
                "delete_team_competition",
                "Can delete Команда from Соревнование",
            ),
        ]

    def __str__(self):
        return self.title

    def period_duration(self):
        """
        Функция рассчитывает длительность турнира.
        """
        duration = self.date_end - self.date_start
        return pluralize_days(duration.days + 1)

    @property
    def is_in_process(self) -> bool:
        """Возвращает True, если соревнование сейчас идет."""
        return self.date_start <= get_now_day() <= self.date_end

    @property
    def is_started(self) -> bool:
        """Проверяет, прошла ли дата начала соревнования."""
        return self.date_start < get_now_day()

    @property
    def is_ended(self) -> bool:
        """Проверяет, прошла ли дата окончания соревнования."""
        return self.date_end < get_now_day()
