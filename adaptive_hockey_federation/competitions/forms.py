from django import forms
from main.forms import CityChoiceField
from competitions.models import Competition
from main.models import Team


class CompetitionForm(forms.ModelForm):
    """Форма для соревнований."""

    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)

    title = forms.CharField(label="Название")
    city = CityChoiceField
    teams = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Команда",
        empty_label="Выберите команду",
        error_messages={"required": "Пожалуйста, выберите команду из списка."},
    )
    date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        ),
        label="Дата начала",
        required=True,
        error_messages={"required": "Пожалуйста, укажите дату начала."},
    )
    date_end = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        ),
        label="Дата завершения",
        required=True,
        error_messages={"required": "Пожалуйста, укажите дату завершения."},
    )

    class Meta:
        model = Competition
        fields = ["title", "city", "teams", "date_start", "date_end"]
