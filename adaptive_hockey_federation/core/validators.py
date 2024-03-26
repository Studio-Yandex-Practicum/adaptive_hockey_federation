import datetime

from core.constants import MAX_AGE_PlAYER, MIN_AGE_PlAYER, FILE_RESOLUTION, MAX_UPLOAD_SIZE
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.files.uploadedfile import InMemoryUploadedFile


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

    if not (min_date <= value <= max_date):
        raise ValidationError(
            f"Возраст должен быть от {MIN_AGE_PlAYER} до {MAX_AGE_PlAYER} лет"
        )


def validate_file(file: InMemoryUploadedFile):
    if file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(
            ("Размер файла должен быть не более  %(size)s MB."),
            params={'size': MAX_UPLOAD_SIZE}, code='invalid_size'
        )

    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in FILE_RESOLUTION:
        raise ValidationError(
            ("Расширение файла '%(ext)s' не допускается. "
             "Пожалуйста, загрузите файл с одним из "
             "следующих расширений: %(ext_list)s."
            ),
            params={
                'ext': file_extension,
                'ext_list': ', '.join(FILE_RESOLUTION)
            },
            code='invalid_extension'
        )