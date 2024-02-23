from core.constants import BLANK_CHOICE, TIMESPAN_CHOICES
from django import forms
from main.models import City, DisciplineName


class AnalyticsFilterForm(forms.Form):
    timespan = forms.ChoiceField(
        choices=(BLANK_CHOICE + list(TIMESPAN_CHOICES)),
        required=False,
        label='За время',
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Все",
    )
    discipline = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Все",
    )

    class Meta:
        fields = ('timespan', 'city', 'discipline')
