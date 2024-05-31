from main.models import DisciplineName
from tests.model_schemas.fields_validation_schemas import (
    ALL_LETTERS, CORRECT_CREATE, CORRECT_UPDATE, FIGURES_AND_LETTERS, LONG_256,
    LONGER_THEN_256, NULL, PUNCTUATION_MARKS_ONLY)

DISCIPLINE_LEVEL_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Наименование дисциплины или статуса дисциплины",
        "discipline_name": DisciplineName,
    },
    CORRECT_UPDATE: {
        "name": "Новое наименование дисциплины или статуса дисциплины",
        "discipline_name": DisciplineName,
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_256,
                NULL,
                PUNCTUATION_MARKS_ONLY,
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
