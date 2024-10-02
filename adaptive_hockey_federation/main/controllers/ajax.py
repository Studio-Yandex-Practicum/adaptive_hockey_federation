from django.http import JsonResponse

from main.models import DisciplineLevel, DisciplineName


def load_discipline_levels(request):
    """
    Представление для получения списка уровней дисциплин по ID дисциплины.

    Используется в формах создания/редактирования данных игрока.
    """
    discipline_level_id = request.GET.get("discipline_level_id")
    try:
        discipline_statuses = DisciplineLevel.objects.filter(
            discipline_name_id=discipline_level_id,
        ).all()
    except ValueError:
        return JsonResponse([], safe=False)
    else:
        return JsonResponse(
            list(discipline_statuses.values("id", "name")),
            safe=False,
        )


def filter_discipline_search(request):
    """Представления для поиска, получения списка дисциплин."""
    disciplines = DisciplineName.objects.all().values("name")
    return JsonResponse(list(disciplines), safe=False)
