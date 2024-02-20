from datetime import datetime

from analytics.forms import AnalyticsFilterForm
from core.constants import GENDER_CHOICES, PLAYER_POSITION_CHOICES
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from main.models import City, Diagnosis, Player, Team
from views import PlayersListView


class AnalyticsListView(
    PlayersListView,
):
    template_name = "analytics/analytics.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        or_lookup = {
            'discipline__discipline_name_id':
                self.request.GET.get('discipline'),
            'team': self.request.GET.get('team'),
            'position': dict(PLAYER_POSITION_CHOICES)[
                self.request.GET.get('position')],
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
                ("команд", Team.objects.count()),
                ("городов", City.objects.count()),
            ],
            "secondary": [
                ("мальчиков", Player.objects.filter(
                    gender=GENDER_CHOICES[0][1]).count()),
                ("девочек", Player.objects.filter(
                    gender=GENDER_CHOICES[1][1]).count()),
                ("младше 18", Player.objects.filter(
                    birthday__lt=date_18_years_ago).count()),
                ("старше 18", Player.objects.filter(
                    birthday__gte=date_18_years_ago).count()),
            ],
            "diagnosis": [
                (f"{diagnosis.name}", diagnosis.player_diagnosis.count())
                for i, diagnosis in enumerate(
                    Diagnosis.objects.all()
                )
            ]
        }
        context["filter_menus"] = {
            ""
        }
        return context
