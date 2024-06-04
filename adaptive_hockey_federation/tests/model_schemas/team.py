from main.models import City, DisciplineName
from tests.model_schemas.fields_validation_schemas import (
    ALL_LETTERS, CORRECT_CREATE, CORRECT_UPDATE, FIGURES_AND_LETTERS,
    FIGURES_ONLY, NULL, PUNCTUATION_MARKS_ONLY, SPACES, THE_ONLY_LETTER)

TEAM_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Команда молодости нашей",
        "city": City,
        "discipline_name": DisciplineName,
    },
    CORRECT_UPDATE: {
        "name": "Команда мечты",
        "city": City,
        "discipline_name": DisciplineName,
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                NULL,
                PUNCTUATION_MARKS_ONLY,
                FIGURES_ONLY,
                THE_ONLY_LETTER,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (ALL_LETTERS, FIGURES_AND_LETTERS, SPACES),
        },
    ),
}
