from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import City, Team


class Event(models.Model):
    """
    Модель соревнований.
    """
    title = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField()
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name=_('Город проведения соревнований'),
        help_text=_('Город проведения соревнований')
    )
    location = models.CharField(max_length=100)
    teams = models.ManyToManyField(
        Team,
        related_name='event_teams',
        verbose_name=_('Состав команд участников'),
        help_text=_('Состав команд участников'),
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        ordering = ('-date_start',)

    def __str__(self):
        return self.title

    def period_duration(self):
        """
        Функция расчитывает длительность турнира
        """
        return self.date_end - self.date_start
