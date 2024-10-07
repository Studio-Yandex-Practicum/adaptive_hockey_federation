import re


def validate_registr_diagnosis(diagnosis: str) -> str:
    """
    Метод, проверяющий диагноз на соответствие коду МКБ-10.

    Если нет, то возвращает диагноз с заглавной буквы.
    """
    pattern = r"^([A-Z]\d{2})(.\d)?$"

    if not re.match(pattern, diagnosis):
        return diagnosis.capitalize()
    return diagnosis
