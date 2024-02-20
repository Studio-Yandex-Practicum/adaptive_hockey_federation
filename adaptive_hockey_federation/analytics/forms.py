from core.constants import (
    BLANK_CHOICE,
    PLAYER_POSITION_CHOICES,
    TIMESPAN_CHOICES,
)
from django import forms
from main.models import DisciplineName, Team


class AnalyticsFilterForm(forms.Form):
    timespan = forms.ChoiceField(
        choices=(BLANK_CHOICE + list(TIMESPAN_CHOICES)),
        required=False,
        label='За время',
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    discipline = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Все",
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Все",
    )
    position = forms.ChoiceField(
        choices=(BLANK_CHOICE + list(PLAYER_POSITION_CHOICES)),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        fields = ('timespan', 'discipline', 'team', 'position')
