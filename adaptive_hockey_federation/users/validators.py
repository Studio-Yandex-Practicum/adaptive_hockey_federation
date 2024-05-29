import re

from django.core.exceptions import ValidationError


def zone_code_without_seven_hundred(phone):

    pattern = r"^(8\s?\(?7|\+?7\s?\(?7).*$"

    if re.match(pattern, phone):

        raise ValidationError(
            "Выберете код в 8 (***) в из следующих вариантов:"
            "3**, 4**, 8**, 9**.",
        )
