from django.db.models import Q


def checking_value(input_value: str) -> str:
    if input_value.isdigit():
        return str(int(input_value))
    return input_value


def create_lookup_all(value: tuple, search: str) -> Q:
    or_lookup_all = Q()
    if isinstance(value[0], tuple):
        or_lookup_all_inside = Q()
        for inside in value:
            or_lookup_all_inside |= Q((inside[0], checking_value(search)))

        or_lookup_all |= or_lookup_all_inside
    else:
        or_lookup_all |= Q((value[0], checking_value(search)))
    return or_lookup_all


def create_lookup_select(value: tuple, dict_param: dict) -> Q:
    def select_value(valueA, valueB):
        return checking_value(valueB if valueB else valueA)

    or_lookup_select = Q()
    if isinstance(value[0], tuple):
        or_lookup_inside: Q = Q()
        for inside in value:
            i_private_expression = inside[1]
            i_parametr = inside[2]
            i_comparison = inside[3]
            if i_parametr in dict_param:
                or_lookup_inside &= Q(
                    (
                        i_private_expression,
                        select_value(dict_param[i_parametr][0], i_comparison),
                    )
                )
        or_lookup_select |= or_lookup_inside
    else:
        expression = value[0]
        parametr = value[2]
        comparison = value[3]
        or_lookup_select |= Q(
            (expression, select_value(dict_param[parametr][0], comparison))
        )
    return or_lookup_select


def models_get_queryset(model, dict_param, queryset, search_fields):
    search_column_name: str = dict_param["search_column"][0]
    or_lookup: Q = Q()
    if search_column_name.lower() in ["все", "all"]:
        search = dict_param["search"][0]
        for value in search_fields.values():
            or_lookup |= create_lookup_all(value, search)
    else:
        or_lookup |= create_lookup_select(
            search_fields[search_column_name], dict_param
        )

    if queryset:
        return queryset.filter(or_lookup)
    else:
        return model.objects.filter(or_lookup)


def analytics_get_queryset(model, dict_param, queryset, search_fields):
    or_lookup: Q = Q()
    for key, value in dict_param.items():
        or_lookup &= Q((search_fields[key], value[0]))

    if queryset:
        queryset = queryset.filter(or_lookup)
    else:
        queryset = model.objects.filter(or_lookup)

    return queryset


def users_get_queryset(model, dict_param, queryset):
    if "search" in dict_param:
        search = dict_param["search"][0]
        search_column = dict_param["search_column"][0]
        if not search_column or search_column.lower() in ["все", "all"]:
            or_lookup = (
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(patronymic__icontains=search)
                | Q(date_joined__icontains=search)
                | Q(role__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
            )
            if queryset:
                queryset = queryset.filter(or_lookup)
            else:
                model.objects.filter(or_lookup)
        else:
            search_fields = {
                "date": "date_joined",
                "role": "role",
                "email": "email",
                "phone": "phone",
            }
            lookup = {f"{search_fields[search_column]}__icontains": search}
            if queryset:
                queryset = queryset.filter(**lookup)
            else:
                queryset = model.objects.filter(**lookup)
    return queryset


def model_get_queryset(page_name, model, dict_param, queryset):
    if page_name == "users":
        return users_get_queryset(model, dict_param, queryset)
