from django import forms
from main.models import Player, Team


class PlayerForm(forms.ModelForm):
    identity_document = forms.CharField(
        widget=forms.TextInput,
        label='Удостоверение личности',
        help_text='Удостоверение личности'
    )
    level_revision = forms.CharField(
        widget=forms.TextInput,
        label='Уровень ревизии',
        help_text='Уровень ревизии',
    )

    class Meta:
        model = Player
        fields = [
            "surname",
            "name",
            "patronymic",
            "gender",
            "birthday",
            "discipline",
            "diagnosis",
            "level_revision",
            "identity_document",
            "team",
            "is_captain",
            "is_assistent",
            "position",
            "number",
            "identity_document",
        ]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'city',
            'staff_team_member',
            'discipline_name',
            'curator'
        ]
