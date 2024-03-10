from competitions.utils import pluralize_days
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

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"
        ordering = ("date_start",)
        permissions = [
            ("list_view_competition", "Can view list of Соревнование"),
            ("list_team_competition", "Can view list of Команда on Соревнование"),
            ("delete_team_competition", "Can delete Команда from Соревнование"),
        ]

    def __str__(self):
        return self.title

    def period_duration(self):
        """
        Функция расчитывает длительность турнира
        """
        duration = self.date_end - self.date_start
        return pluralize_days(duration.days)
