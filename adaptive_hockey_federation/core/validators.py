import datetime

from core.constants import AgeLimits
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


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
