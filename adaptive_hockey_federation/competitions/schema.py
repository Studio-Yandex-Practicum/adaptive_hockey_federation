from django.urls import reverse


def get_competitions_table_data(competitions):
    table_data = []
    for competition in competitions:
        table_data.append(
            {
                "pk": competition.pk,
                "disciplines": ", ".join(
                    competition.disciplines.values_list("name", flat=True),
                ),
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
                        "competitions:competition_id",
                        args=[competition.pk],
                    ),
                },
            },
        )
    return table_data


def get_competitions_table_head():
    return {
        "pk": "Nr.",
        "disciplines": "Дисциплины",
        "date": "Начало соревнований",
        "date_end": "Конец соревнований",
        "title": "Наименование",
        "city": "Город",
        "duration": "Длительность",
        "is_active": "Активно",
        "teams": "Участники",
    }
