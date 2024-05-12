from analytics.schema import ANALYTICS_SEARCH_FIELDS
from django.db.models import Case, F, Q, Value, When
from django.db.models.functions import Now
from django.db.models.lookups import GreaterThan, LessThan
from main.schemas.player_schema import SEARCH_FIELDS


def checking_value(input_value: str) -> str:
    """Функция проверки значения. Если цифровое - уберем нули слева"""
    if input_value.isdigit():
        return str(int(input_value))
    return input_value


def create_lookup_all(dict_param) -> Q:
    """Функция создания запроса по всем полям"""
    or_lookup_all: Q = Q()
    search = dict_param["search"][0]
    for key, value in SEARCH_FIELDS.items():
        if key == "birthday":
            for choice in value:
                or_lookup_all |= Q((f"birthday__{choice}__icontains", search))
        else:
            or_lookup_all |= Q((f"{value}__icontains", search))

    return or_lookup_all


def players_get_queryset(model, dict_param, queryset):
    """Функция создания запроса для игроков"""
    or_lookup: Q = Q()
    search_column_name: str = dict_param["search_column"][0]
    if search_column_name.lower() in ["все", "all"]:
        or_lookup |= create_lookup_all(dict_param)
    elif search_column_name == "birthday":
        for choice in SEARCH_FIELDS["birthday"]:
            if choice in dict_param:
                or_lookup &= Q(
                    (f"birthday__{choice}__exact", int(dict_param[choice][0]))
                )
    elif search_column_name == "gender":
        if "gender" in dict_param:
            or_lookup |= Q(("gender__icontains", dict_param["gender"][0]))
    elif dict_param.get("search"):
        search = dict_param["search"][0]
        or_lookup |= Q(
            (f"{SEARCH_FIELDS[search_column_name]}__icontains", search)
        )
    else:
        return model.objects.all()

    if queryset:
        return queryset.filter(or_lookup)
    else:
        return model.objects.filter(or_lookup)


def analytics_get_queryset(model, dict_param, queryset):
    """Функция создания запроса для аналитики"""
    or_lookup: Q = Q()
    for key, value in ANALYTICS_SEARCH_FIELDS.items():
        if key in dict_param:
            or_lookup &= Q((value, checking_value(dict_param[key][0])))

    if queryset:
        queryset = queryset.filter(or_lookup)
    else:
        queryset = model.objects.filter(or_lookup)

    return queryset


def users_get_queryset(model, dict_param, queryset):
    search_column = dict_param.get("search_column")[0]
    search = dict_param.get("search")
    if search_column:
        if search_column == "name" and search:
            queryset = queryset.filter(
                Q(first_name__icontains=search[0])
                | Q(last_name__icontains=search[0])
                | Q(patronymic__icontains=search[0])
            )
        elif search_column == "date":
            search = ["year", "month", "day"]
            lookup = {
                f"date_joined__{key}__icontains": val[0].lstrip("0")
                for key, val in dict_param.items() if key in search
            }
            if queryset:
                queryset = queryset.filter(**lookup)
            else:
                queryset = model.objects.filter(**lookup)
        else:
            lookup = {f"{search_column}__icontains": search[0]}
            if queryset:
                queryset = queryset.filter(**lookup)
            else:
                queryset = model.objects.filter(**lookup)
    return queryset


def teams_get_queryset(model, dict_param, queryset):
    filter = {
        "city": "city__id",
        "discipline": "discipline_name__in",
        "name": "name__icontains",
    }
    lookup = {}
    for param_key, param_value in dict_param.items():
        if any(len(value) > 0 for value in param_value):
            param = filter.get(param_key)
            if param is not None:
                lookup[param] = param_value[0]
    if queryset:
        queryset = queryset.filter(**lookup)
    else:
        queryset = model.objects.filter(**lookup)

    return queryset


def competitions_get_queryset(model, dict_param, queryset):
    if not queryset:
        queryset = model.objects.all()
    search_column = dict_param.get("search_column")[0]
    search = dict_param.get("search")[0]
    if search_column:
        if search_column == "title":
            queryset = queryset.filter(title__icontains=search)
        elif search_column == "city":
            queryset = queryset.filter(city__name__icontains=search)
        elif search_column == "disciplines":
            queryset = queryset.filter(disciplines__name__icontains=search)
        elif search_column == "is_active":
            queryset = queryset.annotate(
                is_active_view=Case(
                    When(
                        LessThan(F("date_start"), Now())
                        & GreaterThan(F("date_end"), Now()),
                        then=Value("true"),
                    ),
                    default=Value("false"),
                )
            ).filter(is_active_view__icontains=dict_param["active"])
        elif search_column == "teams":
            queryset = queryset.filter(teams__name__icontains=search)
        elif search_column == "date":
            queryset = queryset.filter(
                Q(date_start__year__icontains=dict_param["year"])
                & Q(date_start__month__icontains=dict_param["month"
                                                            ].lstrip("0")
                    )
                & Q(date_start__day__icontains=dict_param["day"].lstrip("0"))
            )
        elif search_column == "date_end":
            queryset = queryset.filter(
                Q(date_end__year__icontains=dict_param["year"])
                & Q(
                    date_end__month__icontains=dict_param["month"].lstrip("0")
                )
                & Q(date_end__day__icontains=dict_param["day"].lstrip("0"))
            )
    return queryset


def model_get_queryset(page_name, model, dict_param, queryset):
    if page_name == "analytics":
        return analytics_get_queryset(model, dict_param, queryset)
    elif page_name == "competitions":
        return competitions_get_queryset(model, dict_param, queryset)
    elif page_name == "players":
        return players_get_queryset(model, dict_param, queryset)
    elif page_name == "teams":
        return teams_get_queryset(model, dict_param, queryset)
    if page_name == "users":
        return users_get_queryset(model, dict_param, queryset)
