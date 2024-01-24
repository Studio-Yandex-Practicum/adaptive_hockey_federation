from django import forms
from main.models import Team, Player


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


class PlayerForm(forms.ModelForm):
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
            "document",
        ]
