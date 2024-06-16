from django import forms
from django.contrib import admin

from games.constants import NumericalValues, Errors
from games.models import Game, GameTeam, GamePlayer
from main.models import Team


class GameTeamAdminForm(forms.ModelForm):
    """
    Кастомная админ-форма для модели GameTeam.

    Включает в себя проверку корректности ввода команд.
    """

    class Meta:
        model = Game
        fields = ("name",)

    def clean(self):
        """Метод, проверяющий корректность ввода команд."""
        form_data = self.data
        if form_data.get(
            "game_teams-0-name",
        ) == form_data.get(
            "game_teams-1-name",
        ):
            raise forms.ValidationError(Errors.CANNOT_PLAY_GAME_AGAINST_SELF)
        elif "game_teams-2-name" in form_data:
            #  На случай появления в форме трёх и более команд
            raise forms.ValidationError(Errors.NO_MORE_THAN_TWO_TEAMS_IN_GAME)
        return self.cleaned_data


class GameTeamsInLine(admin.StackedInline):
    """Инлайн для команд, участвующих в игре."""

    model = GameTeam
    form = GameTeamAdminForm
    extra = NumericalValues.ADMIN_EXTRA_TEAMS
    max_num = NumericalValues.MAX_TEAMS_IN_GAME
    min_num = max_num
    readonly_fields = ("discipline_name",)


class GamePlayersInLine(admin.TabularInline):
    """Инлайн для игроков, участвующих в игре."""

    model = GamePlayer
    extra = 0
    readonly_fields = ("name", "number", "game_team")
    can_delete = False


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Админка для модели игр."""

    list_display = ("name", "date", "competition", "video_link")
    list_filter = ("date", "competition")
    search_fields = ("name",)
    ordering = ["name"]
    inlines = [GameTeamsInLine]

    def save_model(self, request, obj, form, change):
        """
        Сохраняет модель игры и связанные с ней модели игроков и команд.

        Дополнительно передаём список команд, чтобы их смог получить и
        обработать соответствующий сигнал.
        """
        teams = Team.objects.filter(
            name__in=[
                form.data.get(
                    "game_teams-0-name",
                ),
                form.data.get(
                    "game_teams-1-name",
                ),
            ],
        ).values_list(
            "id",
            flat=True,
        )
        obj.teams = teams
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """
        По умолчанию, сохраняет изменения, указанные в inline formset'е.

        В нашем случае в этом нет необходимости, так как созданием связанных
        GameTeam и GamePlayers занимаются сигналы, поэтому мы формально
        сохраняем изменения, чтобы вызывать сигналы, которые и проведут
        необходимые операции. Сами данные из формы будут сброшены.
        Если этого не делать, то при сохранении формы возникнут дубликаты
        сущностей GameTeam и GamePlayers.
        """
        formset.save(commit=False)


@admin.register(GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    """Админка для модели команды, участвующей в игре."""

    list_display = ("name", "discipline_name", "game")
    list_filter = ("game",)
    search_fields = ("name",)
    ordering = ["name"]
    inlines = [GamePlayersInLine]


@admin.register(GamePlayer)
class GamePlayerAdmin(admin.ModelAdmin):
    """Админка для модели игроков, участвующих в игре."""

    list_display = ("name", "number", "game_team")
    list_filter = ("game_team",)
    search_fields = ("name",)
    ordering = ["name"]
