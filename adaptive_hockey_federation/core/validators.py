import datetime

from core.constants import MAX_AGE_PlAYER, MIN_AGE_PlAYER
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
    min_date = datetime.date(now.year - MAX_AGE_PlAYER, now.month, now.day)
    max_date = datetime.date(now.year - MIN_AGE_PlAYER, now.month, now.day)

    if not (min_date <= value <= max_date):
        raise ValidationError(
            f"Возраст должен быть от {MIN_AGE_PlAYER} до {MAX_AGE_PlAYER} лет",
        )


def validate_game_date(date: datetime.date) -> datetime.date:
    """Проверка валидности даты игры. Дата не должна быть больше текущей."""
    if date > django_now():
        raise ValidationError("Игра не может проходить в будущем")
    return date
