from tests.model_schemas.fields_validation_schemas import (
    ALL_CAPS,
    ALL_LOWER,
    CORRECT_CREATE,
    CORRECT_PHONE,
    CORRECT_UPDATE,
    DOUBLE_LAST_NAME,
    DOUBLE_PATRONYMIC,
    FIGURES_AND_LETTERS,
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
)

STAFF_MEMBER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Василий",
        "surname": "Иванович",
        "patronymic": "Петров",
        "phone": "+7 990 060-45-71",
    },
    CORRECT_UPDATE: {
        "name": "Бурямглоюнебокроетвихриснежныекрутятокакзверьоназавоет",
        "surname": "Съешьещеэтихмягкихфранцузскихбулочекдавыпейчаюев",
        "patronymic": "Кракозябробормоглототроглодитобрандашмыгович",
        "phone": "+7 990 060-45-72",
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
        {"fields": "phone", "test_values": (INCORRECT_PHONE,)},
    ),
    "must_be_admitted": (
        {
            "fields": ("surname", "name", "patronymic"),
            "test_values": (THE_ONLY_CYR_LETTER,),
        },
        {"fields": "surname", "test_values": (DOUBLE_LAST_NAME,)},
        {"fields": "patronymic", "test_values": (DOUBLE_PATRONYMIC,)},
        {"fields": "phone", "test_values": (CORRECT_PHONE,)},
    ),
}
