from datetime import datetime

from core.constants import GENDER_CHOICES
from dateutil.relativedelta import relativedelta
from main.models import City, Diagnosis, Player, Team
from views import PlayersListView


class AnalyticsListView(
    PlayersListView,
):
    template_name = "main/analytics/analytics.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        date_18_years_ago = datetime.now() - relativedelta(years=18)
        context["dashboard"] = {
            "primary": [
                ("игроков", Player.objects.count()),
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
