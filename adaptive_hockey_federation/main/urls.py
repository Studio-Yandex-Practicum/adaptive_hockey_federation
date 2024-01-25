from django.urls import path
from main import views

app_name = "main"


urlpatterns = [
    path("", views.main, name="main"),
    path("players/", views.PlayersListView.as_view(), name="players"),
    path("players/<int:id>/", views.PlayerIdView.as_view(), name="player_id"),
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
        "team_update/<int:team_id>/",
        views.UpdateTeamView.as_view(),
        name="team_update"
    ),
    path(
        "team_delete/<int:team_id>/",
        views.DeleteTeamView.as_view(),
        name="team_delete"
    ),
    path("team_create/", views.CreateTeamView.as_view(), name="team_create"),
    path(
        "competitions/<int:id>/",
        views.competitions_id,
        name="competitions_id",
    ),
    path("competitions/", views.competitions, name="competitions"),
    path("analytics/", views.analytics, name="analytics"),
    path("unloads/", views.unloads, name="unloads"),
]
