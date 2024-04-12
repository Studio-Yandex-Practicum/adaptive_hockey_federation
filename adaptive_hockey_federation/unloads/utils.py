from django.db.models import Q
from main.schemas.player_schema import SEARCH_FIELDS


def players_get_queryset(model, dict_param, queryset):
    """Функция поиска для игроков"""
    if "search" in dict_param:
        search = dict_param["search"][0]
        search_column = dict_param["search_column"][0]
        if not search_column or search_column.lower() in ["все", "all"]:
            or_lookup = (
                Q(surname__icontains=search)
                | Q(name__icontains=search)
                | Q(birthday__icontains=search)
                | Q(gender__icontains=search)
                | Q(number__icontains=search)
                | Q(discipline__discipline_name_id__name__icontains=search)
                | Q(diagnosis__name__icontains=search)
            )
            if queryset:
                queryset = queryset.filter(or_lookup)
            else:
                model.objects.filter(or_lookup)
        else:
            search_fields = SEARCH_FIELDS
            lookup = {f"{search_fields[search_column]}__icontains": search}
            if queryset:
                queryset = queryset.filter(**lookup)
            else:
                queryset = model.objects.filter(**lookup)
    return queryset


def analytics_get_queryset(model, dict_param, queryset):
    """Функция поиска для аналитики"""
    keys_param = ("timespan", "birthday", "discipline", "city")
    if not any(elem in dict_param for elem in keys_param):
        return queryset

    timespan = None
    birthday = None
    discipline = None
    city = None
    if "timespan" in dict_param:
        timespan = dict_param["timespan"][0]
    if "birthday" in dict_param:
        birthday = dict_param["birthday"][0]
    if "discipline" in dict_param:
        discipline = dict_param["discipline"][0]
    if "city" in dict_param:
        city = dict_param["city"][0]

    or_lookup = {
        "addition_date__gte": timespan,
        "birthday__year": birthday,
        "discipline__discipline_name_id": discipline,
        "team__city": city,
    }
    or_lookup = {key: value for key, value in or_lookup.items() if value}
    if queryset:
        queryset = queryset.filter(Q(**or_lookup))
    else:
        queryset = model.objects.filter(Q(**or_lookup))

    return queryset


def model_get_queryset(page_name, model, dict_param, queryset):
    if page_name == "players":
        return players_get_queryset(model, dict_param, queryset)
    elif page_name == "analytics":
        return analytics_get_queryset(model, dict_param, queryset)
