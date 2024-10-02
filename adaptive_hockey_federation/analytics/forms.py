import datetime

from django import forms
from django.db.models.functions import ExtractYear
from main.models import City, DisciplineName, Player


class AnalyticsFilterForm(forms.Form):
    """Класс-форма для фильтрации страницы с аналитикой."""

    birthday = forms.ModelChoiceField(
        queryset=Player.objects.dates("birthday", "year").values_list(
            ExtractYear("birthday"),
            flat=True,
        ),
        required=False,
        label="Год рождения",
        widget=forms.Select(attrs={"class": "form-control arrow-before"}),
        empty_label="Все",
    )
    timespan = forms.ChoiceField(
        choices=[],
        required=False,
        label="За время",
        widget=forms.Select(attrs={"class": "form-control arrow-before"}),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        label="Город",
        widget=forms.Select(attrs={"class": "form-control arrow-before"}),
        empty_label="Все",
    )
    discipline = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all(),
        required=False,
        label="Дисциплина",
        widget=forms.Select(attrs={"class": "form-control arrow-before"}),
        empty_label="Все",
    )

    class Meta:
        fields = ("birthday", "timespan", "city", "discipline")

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации экземпляра класса.

        Вызывает метод, добавляющий в поле timespan выбор
        временного интервала для фильтрации.
        """
        super().__init__(*args, **kwargs)
        self.set_timespan_choices()

    def set_timespan_choices(self):
        """
        Метод, добавляющий выбор временного интервала для фильтрации.

        1. За все время
        2. За текущий месяц
        3. За текущий год.
        """
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
