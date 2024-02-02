from django.urls import path
from events import views as events
from main import views

app_name = "main"


urlpatterns = [
    path("", views.main, name="main"),
    path("players/", views.PlayersListView.as_view(), name="players"),
    path("players/<int:id>/", views.PlayerIdView.as_view(), name="player_id"),
    path("teams/", views.TeamListView.as_view(), name="teams"),
    path("teams/<int:team_id>/", views.TeamIdView.as_view(), name="teams_id"),
    path(
        "competitions/<int:id>/",
        views.competitions_id,
        name="competitions_id",
    ),
    path("competitions/", events.EventListView.as_view(), name="competitions"),
    path("analytics/", views.analytics, name="analytics"),
    path("unloads/", views.unloads, name="unloads"),
]
