from django.core.exceptions import ValidationError


def zone_code_without_seven_hundred(phone):
    if (
        phone[0:2] == "87" or phone[0:3] == "8 7" or phone[0:4] == "8 (7"
        or phone[0:3] == "+77" or phone[0:4] == "+7 7" or phone[0:5] == "+7 (7"
    ):
        raise ValidationError(
            "Выберете код в 8 (***) в из следующих вариантов:"
            "3**, 4**, 8**, 9**."
        )
