from analytics.forms import AnalyticsFilterForm
from core.constants import GENDER_CHOICES
from main.models import Nosology, Team


def analytics_table(self, context, date_18_years_ago):
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
