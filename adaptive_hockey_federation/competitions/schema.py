from django.urls import reverse


def competitions_table(context):
    competitions = context["competitions"]
    table_data = []
    for competition in competitions:
        table_data.append(
            {
                "pk": competition.pk,
                "data": competition.date_start,
                "data_end": competition.date_end,
                "title": competition.title,
                "city": competition.city,
                "duration": competition.period_duration,
                "is_active": competition.is_in_process,
                "_ref_": {
                    "name": "Участники",
                    "type": "button",
                    "url": reverse(
                        "competitions:competitions_id",
                        args=[competition.pk],
                    ),
                },
            }
        )

    context["table_head"] = {
        "pk": "Nr.",
        "data": "Начало соревнований",
        "data_end": "Конец соревнований",
        "title": "Наименование",
        "city": "Город",
        "duration": "Длительность",
        "is_active": "Активно",
        "teams": "Участники",
    }
    context["table_data"] = table_data
    return context
