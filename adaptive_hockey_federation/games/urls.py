from django.urls import include, path

from games import views

app_name = "games"

games_urlpattern = [
    path("", views.GamesListView.as_view(), name="games"),
    path("create/", views.GameCreateView.as_view(), name="game_create"),
    path(
        'edit_numbers/<int:game_team>/',
        views.EditTeamPlayersNumbersView.as_view(),
        name='edit_team_players_numbers'
    ),
    path(
        "<int:game_id>/edit/",
        views.GameEditView.as_view(),
        name="game_edit",
    ),
    path(
        "<int:game_id>/delete/",
        views.GameDeleteView.as_view(),
        name="game_delete",
    ),
    path(
        "<int:game_id>/info-about-game/",
        views.GamesInfoView.as_view(),
        name="game_info",
    ),
]

urlpatterns = [
    path("games/", include(games_urlpattern)),
]
