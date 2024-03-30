from datetime import datetime

from analytics import schema
from core.permissions import AdminRequiredMixin
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from main.controllers.player_views import PlayersListView


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
        context = schema.analytics_table(self, context, date_18_years_ago)
        return context
