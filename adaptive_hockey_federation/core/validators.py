import datetime

from core.constants import MAX_AGE_PlAYER, MIN_AGE_PlAYER
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def fio_validator() -> RegexValidator:
    """Функция проверки поля на присутствие только
    кирилических символов. Возможно использование дефиса.
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

    if not (min_date < value < max_date):
        raise ValidationError(
            f"Возраст должен быть от {MIN_AGE_PlAYER} до {MAX_AGE_PlAYER} лет"
        )
