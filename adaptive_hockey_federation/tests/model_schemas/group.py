from tests.model_schemas.fields_validation_schemas import (
    CORRECT_CREATE,
    CORRECT_UPDATE,
    LONG_150,
    LONGER_THEN_150,
    NULL,
)

GROUP_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Группа в полосатых купальниках",
    },
    CORRECT_UPDATE: {
        "name": "Группа крови на рукаве",
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_150,
                NULL,
            ),
        },
    ),
    "must_be_admitted": ({"fields": "name", "test_values": (LONG_150,)},),
}
