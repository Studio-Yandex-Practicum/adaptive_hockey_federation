from main.models import DisciplineLevel, DisciplineName
from tests.model_schemas.fields_validation_schemas import (
    CORRECT_CREATE,
    CORRECT_UPDATE,
)

DISCIPLINE_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "discipline_name": DisciplineName,
        "discipline_level": DisciplineLevel,
    },
    CORRECT_UPDATE: {
        "discipline_name": DisciplineName,
        "discipline_level": DisciplineLevel,
    },
}
