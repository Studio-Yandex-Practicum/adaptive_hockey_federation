from tests.model_schemas.fields_validation_schemas import (CORRECT_CITY_NAMES,
                                                           CORRECT_CREATE,
                                                           CORRECT_UPDATE,
                                                           FIGURES_AND_LETTERS,
                                                           FIGURES_ONLY,
                                                           LONG_256,
                                                           LONGER_THEN_256,
                                                           NOT_CYR, NULL)

CITY_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Городкоторогонет",
    },
    CORRECT_UPDATE: {
        "name": "Новыйгородкоторогонет",
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_256,
                NULL,
                NOT_CYR,
                FIGURES_ONLY,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (LONG_256, FIGURES_AND_LETTERS, CORRECT_CITY_NAMES),
        },
    ),
}
