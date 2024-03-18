from datetime import datetime

from analytics.forms import AnalyticsFilterForm
from analytics.mixins import AdminRequiredMixin
from core.constants import GENDER_CHOICES
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from main.controllers.player_views import PlayersListView
from main.models import Nosology, Team


class AnalyticsListView(
    AdminRequiredMixin,
    PlayersListView,
):
    template_name = "analytics/analytics.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        or_lookup = {
            "addition_date__gte": self.request.GET.get("timespan"),
            "birthday__year": self.request.GET.get("birthday"),
            "discipline__discipline_name_id": self.request.GET.get(
                "discipline"
            ),
            "team__city": self.request.GET.get("city"),
        }
        or_lookup = {key: value for key, value in or_lookup.items() if value}
        if not or_lookup:
            return queryset
        return queryset.filter(Q(**or_lookup))

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
