import datetime

from django import forms
from django.db.models.functions import ExtractYear
from main.models import City, DisciplineName, Player


class AnalyticsFilterForm(forms.Form):
    birthday = forms.ModelChoiceField(
        queryset=Player.objects.dates("birthday", "year").values_list(
            ExtractYear("birthday"), flat=True
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Год рождения",
        empty_label="Все",
    )
    timespan = forms.ChoiceField(
        choices=[],
        required=False,
        label="За время",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Город",
        empty_label="Все",
    )
    discipline = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Дисциплина",
        empty_label="Все",
    )

    class Meta:
        fields = ("birthday", "timespan", "city", "discipline")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_timespan_choices()

    def set_timespan_choices(self):
        self.fields["timespan"].choices = (
            (None, "Все"),
            (
                datetime.date.today().replace(
                    day=1,
                ),
                "Текущий месяц",
            ),
            (
                datetime.date.today().replace(
                    month=1,
                    day=1,
                ),
                "Текущий год",
            ),
        )
