from main.models import StaffMember
from tests.model_schemas.fields_validation_schemas import (
    CORRECT_CREATE,
    CORRECT_UPDATE,
    LONGER_THEN_256,
    NULL,
    THE_ONLY_LETTER,
)

STAFF_TEAM_MEMBER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "staff_member": StaffMember,
        "staff_position": "тренер",
        "qualification": "Какаятотамквалификация",
        "notes": "Наш величайший тренер родился еще в те времена, когда...",
    },
    CORRECT_UPDATE: {
        "staff_member": StaffMember,
        "staff_position": "пушер-тьютор",
        "qualification": "Какаятотамещеквалификация",
        "notes": "Этот пушер-тьютор толкает игроков на лед с такой силой...",
    },
    "must_not_be_admitted": (
        {
            "fields": "staff_position",
            "test_values": (
                ("повелительмух", "непредусмотренная позиция сотрудника"),
                NULL,
            ),
        },
        {
            "fields": "qualification",
            "test_values": (LONGER_THEN_256,),
        },
    ),
    "must_be_admitted": (
        {"fields": "qualification", "test_values": (THE_ONLY_LETTER,)},
    ),
}
