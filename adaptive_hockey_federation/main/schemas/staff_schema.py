from django.urls import reverse
from main.models import StaffTeamMember


def staff_list_table(self, context):
    table_head = {}
    for field in self.fields:
        if field != "id":
            table_head[field] = self.model._meta.get_field(field).verbose_name
    context["table_head"] = table_head

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

    context["table_data"] = table_data
    return context


def staff_id_list(self, context) -> dict:
    staff = context["staff"]
    staff_fields = [
        ("Фамилия", staff.surname),
        ("Имя", staff.name),
        ("Отчество", staff.patronymic),
        ("Номер телефона", staff.phone),
    ]

    queryset = StaffTeamMember.objects.filter(staff_member=self.kwargs["pk"])
    team_fields = []
    for staff_team in queryset:
        team_fields.append(
            (
                "Команда",
                ", ".join([team.name for team in staff_team.team.all()]),
            )
        )
        team_fields.append(
            ("Статус сотрудника", staff_team.staff_position),
        )
        team_fields.append(
            ("Квалификация", staff_team.qualification),
        )
        team_fields.append(
            ("Описание", staff_team.notes),
        )
    context["staff_fields"] = staff_fields
    context["team_fields"] = team_fields
    return context
