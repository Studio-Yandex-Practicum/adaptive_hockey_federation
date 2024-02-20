from django.urls import path
from events import views as events
from main import views

app_name = "main"


urlpatterns = [
    path("", views.main, name="main"),
    path("players/", views.PlayersListView.as_view(), name="players"),
    path("players/<int:pk>/", views.PlayerIdView.as_view(), name="player_id"),
    path(
        "players/<int:pk>/edit/",
        views.PlayerIDEditView.as_view(),
        name="player_id_edit",
    ),
    path(
        "players/<int:pk>/delete/",
        views.PlayerIDDeleteView.as_view(),
        name="player_id_delete",
    ),
    path("player_deleted/", views.player_id_deleted, name="player_id_deleted"),
    path("teams/", views.TeamListView.as_view(), name="teams"),
    path("teams/create/", views.CreateTeamView.as_view(), name="team_create"),
    path(
        "teams/<int:team_id>/edit/",
        views.UpdateTeamView.as_view(),
        name="team_update"
    ),
    path(
        "teams/<int:team_id>/delete/",
        views.DeleteTeamView.as_view(),
        name="team_delete"
    ),
    path("teams/<int:team_id>/", views.TeamIdView.as_view(), name="teams_id"),
    path(
        "competitions/<int:pk>/",
        events.TeamsOnEnvent.as_view(), name="competitions_id"
    ),
    path("competitions/", events.EventListView.as_view(), name="competitions"),
    path("analytics/", views.analytics, name="analytics"),
    path("unloads/", views.unloads, name="unloads"),
]
