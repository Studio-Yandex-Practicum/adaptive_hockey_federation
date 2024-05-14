from core.constants import ROLE_AGENT
from tests.model_schemas.fields_validation_schemas import (
    ALL_CAPS,
    ALL_LOWER,
    CORRECT_CREATE,
    CORRECT_PHONE,
    CORRECT_UPDATE,
    DOUBLE_LAST_NAME,
    DOUBLE_PATRONYMIC,
    FIGURES_AND_LETTERS,
    INCORRECT_EMAIL,
    INCORRECT_PHONE,
    LONGER_THEN_256,
    LOWER_SECOND_LAST_NAME,
    MIDDLE_CAP,
    NOT_CYR,
    NULL,
    PUNCTUATION_MARKS_EXCEPT_HYPHEN,
    SPACES,
    THE_ONLY_CYR_LETTER,
    TWO_OR_MORE_SPACES,
    UNFORESEEN_ROLE,
)

USER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "first_name": "Василий",
        "last_name": "Иванович",
        "patronymic": "Петров",
        "role": ROLE_AGENT,
        "email": "fake@fake.com",
        "phone": "+7 990 060-45-71",
        "is_staff": False,
        "password": "pAss9742!word",
    },
    CORRECT_UPDATE: {
        "first_name": "Бурямглоюнебокроетвихриснежныекрутятокакзверьоназавоет",
        "last_name": "Съешьещеэтихмягкихфранцузскихбулочекдавыпейчаюев",
        "patronymic": "Кракозябробормоглототроглодитобрандашмыгович",
        "role": ROLE_AGENT,
        "email": "fake@fake.com",
        "phone": "+7 990 060-45-72",
        "is_staff": False,
        "password": "NewPAss9742!word",
    },
    "must_not_be_admitted": (
        {
            "fields": ("first_name", "last_name", "patronymic"),
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
                "first_name",
                "last_name",
            ),
            "test_values": (NULL,),
        },
        {
            "fields": "last_name",
            "test_values": (LOWER_SECOND_LAST_NAME, SPACES),
        },
        {"fields": "patronymic", "test_values": (TWO_OR_MORE_SPACES,)},
        {"fields": "email", "test_values": (INCORRECT_EMAIL,)},
        {"fields": "role", "test_values": (UNFORESEEN_ROLE,)},
        {"fields": "phone", "test_values": (INCORRECT_PHONE,)},
    ),
    "must_be_admitted": (
        {
            "fields": ("last_name", "first_name", "patronymic"),
            "test_values": (THE_ONLY_CYR_LETTER,),
        },
        {"fields": "last_name", "test_values": (DOUBLE_LAST_NAME,)},
        {"fields": "patronymic", "test_values": (DOUBLE_PATRONYMIC,)},
        {"fields": "phone", "test_values": (CORRECT_PHONE,)},
    ),
}
