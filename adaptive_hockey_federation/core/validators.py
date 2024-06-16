import datetime

from core.constants import AgeLimits
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.timezone import now as django_now


def fio_validator() -> RegexValidator:
    """
    Функция проверки поля.

    1. Присутствие только кирилических символов
    2. Возможно использование дефиса.
    """
    return RegexValidator(
        r"^[А-Яа-яё -]+$",
        (
            "Строка должны состоять из кирилических символов. "
            "Возможно использование дефиса."
        ),
    )


def validate_date_birth(value: datetime.date):
    now = datetime.date.today()
    min_date = datetime.date(
        now.year - AgeLimits.MAX_AGE_PLAYER,
        now.month,
        now.day,
    )
    max_date = datetime.date(
        now.year - AgeLimits.MIN_AGE_PLAYER,
        now.month,
        now.day,
    )

    if not (min_date <= value <= max_date):
        raise ValidationError(
            f"Возраст должен быть от {AgeLimits.MIN_AGE_PLAYER}"
            f"до {AgeLimits.MAX_AGE_PLAYER} лет",
        )


def validate_game_date(date: datetime.date) -> datetime.date:
    """Проверка валидности даты игры. Дата не должна быть больше текущей."""
    if date > django_now():
        raise ValidationError("Игра не может проходить в будущем")
    return date
