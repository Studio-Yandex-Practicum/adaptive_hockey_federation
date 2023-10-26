from django.db import models


class Team(models.Model):
    """Класс команды
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class Position(models.Model):
    """Позиция в команде
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'


class BaseUserInfo(models.Model):
    """Класс игрока
    """
    CLS_CHOICES = [
        ('A', 'A'),
        ('A2', 'A2'),
        ('B', 'B'),
        ('B2', 'B2'),
        ('C', 'C'),
        ('C2', 'C2'),
    ]
    name = models.CharField(
        max_length=56,
        verbose_name='Имя'
    )
    surname: models.CharField(
        max_length=56,
        verbose_name='Фамилия'
    )
    date_of_birth = models.DateTimeField(
        verbose_name='Дата рождения'
    )
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Команда'
    )
    position = models.ForeignKey(
        Team, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Позиция'
    )
    classification = models.CharField(
        max_length=255,
        choices=CLS_CHOICES,
        default=None)
