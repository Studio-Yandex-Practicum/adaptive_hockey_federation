from django.urls import path
from main import views as main_views
from main.controllers import player_views, team_views

app_name = "main"


urlpatterns = [
    path("", main_views.main, name="main"),
    path("players/", player_views.PlayersListView.as_view(), name="players"),
    path(
        "players/<int:pk>/",
        player_views.PlayerIdView.as_view(),
        name="player_id",
    ),
    path(
        "player_create/", player_views.PlayerCreateView.as_view(),
        name="player_create"
    ),
    path(
        "players/<int:pk>/edit/",
        player_views.PlayerIDEditView.as_view(),
        name="player_id_edit",
    ),
    path(
        "players/<int:pk>/delete/",
        player_views.PlayerIDDeleteView.as_view(),
        name="player_id_delete",
    ),
    path(
        "player_deleted/",
        player_views.player_id_deleted,
        name="player_id_deleted",
    ),
    path(
        "player_create/",
        player_views.PlayerCreateView.as_view(),
        name="player_create",
    ),
    path("teams/", team_views.TeamListView.as_view(), name="teams"),
    path(
        "teams/create/",
        team_views.CreateTeamView.as_view(),
        name="team_create",
    ),
    path(
        "teams/<int:team_id>/edit/",
        team_views.UpdateTeamView.as_view(),
        name="team_update",
    ),
    path(
        "teams/<int:team_id>/delete/",
        team_views.DeleteTeamView.as_view(),
        name="team_delete",
    ),
    path(
        "teams/<int:team_id>/",
        team_views.TeamIdView.as_view(),
        name="teams_id",
    ),
    path("unloads/", main_views.unloads, name="unloads"),
]
