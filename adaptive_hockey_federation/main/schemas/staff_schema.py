from django.urls import reverse

STAFF_SEARCH_FIELDS = {
    "surname": "surname",
    "name": "name",
    "patronymic": "patronymic",
    "phone": "phone",
}


def get_staff_table_data(context):
    table_data = [
        {
            "surname": staff.surname,
            "name": staff.name,
            "patronymic": staff.patronymic,
            "phone": staff.phone,
            "url": reverse("main:staff_id", args=[staff.id]),
            "id": staff.pk,
        }
        for staff in context["staffs"]
    ]
    return table_data


def get_staff_fields(staff):
    staff_fields = [
        ("Фамилия", staff.surname),
        ("Имя", staff.name),
        ("Отчество", staff.patronymic),
        ("Номер телефона", staff.phone),
    ]
    return staff_fields


def add_pisition_in_context(queryset=None):
    """Функция добавления формы staff_member по позициям в context."""
    team_fields = []
    if queryset.exists():
        for staff_team in queryset:
            team_fields.append((
                "Команда",
                ", ".join(
                    [team.name for team in staff_team.team.all()]
                    if staff_team.team.all().exists() else ["Свободный агент"],
                ),
            ))
            team_fields.append(
                ("Квалификация", staff_team.qualification),
            )
            team_fields.append(
                ("Описание", staff_team.notes),
            )
        return staff_team, team_fields
    return None, None
