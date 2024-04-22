from datetime import datetime

from analytics.forms import AnalyticsFilterForm
from core.constants import GENDER_CHOICES
from core.permissions import AdminRequiredMixin
from dateutil.relativedelta import relativedelta
from django.views.generic.list import ListView
from main.models import Nosology, Player, Team
from main.schemas.player_schema import ANALITICS_SEARCH_FIELDS
from unloads.utils import analytics_get_queryset


class AnalyticsListView(
    AdminRequiredMixin,
    ListView,
):
    template_name = "analytics/analytics.html"
    paginate_by = 10
    # PlayersListView,

    def get_queryset(self):
        queryset = super().get_queryset()
        dict_param = dict(self.request.GET)
        dict_param = {k: v for k, v in dict_param.items() if v != [""]}
        if len(dict_param) > 0:
            queryset = analytics_get_queryset(
                Player, dict_param, queryset, ANALITICS_SEARCH_FIELDS
            )
        return (
            queryset.select_related("diagnosis")
            .select_related("discipline_name")
            .order_by("surname")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        date_18_years_ago = datetime.now() - relativedelta(years=18)
        context["form"] = AnalyticsFilterForm(self.request.GET or None)
        context["dashboard"] = {
            "primary": [
                ("игроков", self.get_queryset().count()),
                (
                    "команд",
                    teams_count := Team.objects.filter(
                        id__in=self.get_queryset()
                        .values_list("team", flat=True)
                        .distinct()
                    ).count(),
                ),
                ("городов", teams_count),
            ],
            "secondary": [
                (
                    "мальчиков",
                    self.get_queryset()
                    .filter(gender=GENDER_CHOICES[0][1])
                    .count(),
                ),
                (
                    "девочек",
                    self.get_queryset()
                    .filter(gender=GENDER_CHOICES[1][1])
                    .count(),
                ),
                (
                    "младше 18",
                    self.get_queryset()
                    .filter(birthday__gte=date_18_years_ago)
                    .count(),
                ),
                (
                    "старше 18",
                    self.get_queryset()
                    .filter(birthday__lt=date_18_years_ago)
                    .count(),
                ),
            ],
            "nosology": [
                (
                    f"{nosology.name}",
                    self.get_queryset()
                    .filter(diagnosis__nosology=nosology)
                    .count(),
                )
                for i, nosology in enumerate(
                    Nosology.objects.filter(
                        diagnosis__in=self.get_queryset()
                        .values_list("diagnosis", flat=True)
                        .distinct()
                    ).distinct()
                )
            ],
        }
        return context
