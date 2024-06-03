from main.models import Diagnosis, DisciplineLevel, DisciplineName
from tests.model_schemas.fields_validation_schemas import (
    ALL_CAPS, ALL_LOWER, ALL_RUS_LETTERS_IN_FIO, CORRECT_CREATE,
    CORRECT_DOC_ID, CORRECT_UPDATE, DOUBLE_LAST_NAME, DOUBLE_PATRONYMIC,
    FIGURES_AND_LETTERS, INCORRECT_DOC_ID, INCORRECT_GENDER_CHOICE,
    INCORRECT_PLAYER_POSITION, LONGER_THEN_256, LOWER_SECOND_LAST_NAME,
    MIDDLE_CAP, NEGATIVE, NOT_CYR, NULL, PUNCTUATION_MARKS_EXCEPT_HYPHEN,
    SPACES, THE_ONLY_CYR_LETTER, TWO_OR_MORE_SPACES)

PLAYER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Василий",
        "surname": "Иванович",
        "patronymic": "Петров",
        "diagnosis": Diagnosis,
        "discipline_name": DisciplineName,
        "discipline_level": DisciplineLevel,
        "birthday": "2010-03-25",
        "gender": "Мужской",
        "level_revision": "Тестовый уровень ревизии.",
        "position": "Поплавок",
        "number": 45,
        "is_captain": False,
        "is_assistent": False,
        "identity_document": "Паспорт 3030 303030",
    },
    CORRECT_UPDATE: {
        "name": "Бурямглоюнебокроетвихриснежныекрутятокакзверьоназавоет",
        "surname": "Съешьещеэтихмягкихфранцузскихбулочекдавыпейчаюев",
        "patronymic": "Кракозябробормоглототроглодитобрандашмыгович",
        "diagnosis": Diagnosis,
        "discipline_name": DisciplineName,
        "discipline_level": DisciplineLevel,
        "birthday": "2009-03-25",
        "gender": "Женский",
        "level_revision": "Какой-то другой тестовый уровень ревизии.",
        "position": "Нападающий",
        "number": 41,
        "is_captain": True,
        "is_assistent": True,
        "identity_document": "Паспорт 4040 404040",
    },
    "must_not_be_admitted": (
        {
            "fields": ("name", "surname", "patronymic"),
            "test_values": (
                ALL_LOWER,
                ALL_CAPS,
                MIDDLE_CAP,
                NOT_CYR,
                FIGURES_AND_LETTERS,
                LONGER_THEN_256,
                PUNCTUATION_MARKS_EXCEPT_HYPHEN,
            ),
        },
        {
            "fields": (
                "name",
                "surname",
            ),
            "test_values": (NULL,),
        },
        {
            "fields": "surname",
            "test_values": (LOWER_SECOND_LAST_NAME, SPACES),
        },
        {"fields": "patronymic", "test_values": (TWO_OR_MORE_SPACES,)},
        {"fields": "identity_document", "test_values": (INCORRECT_DOC_ID,)},
        {"fields": "gender", "test_values": (INCORRECT_GENDER_CHOICE,)},
        {"fields": "position", "test_values": (INCORRECT_PLAYER_POSITION,)},
        {"fields": "number", "test_values": (NEGATIVE,)},
    ),
    "must_be_admitted": (
        {
            "fields": ("surname", "name", "patronymic"),
            "test_values": (THE_ONLY_CYR_LETTER, ALL_RUS_LETTERS_IN_FIO),
        },
        {"fields": "surname", "test_values": (DOUBLE_LAST_NAME,)},
        {"fields": "patronymic", "test_values": (DOUBLE_PATRONYMIC,)},
        {"fields": "identity_document", "test_values": (CORRECT_DOC_ID,)},
    ),
}
