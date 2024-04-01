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
