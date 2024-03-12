from datetime import datetime

from django.core.exceptions import ValidationError


def date_not_before_today(value):
    """Проверка на создание соревнования с датой начала в прошлом.
    Должен вызываться только при создании соревнования."""
    if value < datetime.date(datetime.now()):
        raise ValidationError(
            "Введите дату не позднее сегодняшней.", code="past_is_forbidden"
        )
