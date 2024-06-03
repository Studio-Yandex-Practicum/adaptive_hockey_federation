from tests.model_schemas.fields_validation_schemas import (
    ALL_LETTERS, CORRECT_CREATE, CORRECT_UPDATE, FIGURES_AND_LETTERS,
    FIGURES_ONLY, LONG_256, LONGER_THEN_256, NULL, PUNCTUATION_MARKS_ONLY,
    THE_ONLY_LETTER)

SIMPLE_UNIQUE_NAME_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Какоетоимя",
    },
    CORRECT_UPDATE: {
        "name": "Какоетоновоеимя",
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_256,
                NULL,
                FIGURES_ONLY,
                PUNCTUATION_MARKS_ONLY,
                THE_ONLY_LETTER,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONG_256,
                FIGURES_AND_LETTERS,
                ALL_LETTERS,
            ),
        },
    ),
}
