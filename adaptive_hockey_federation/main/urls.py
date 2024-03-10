from django.urls import include, path
from main import views as main_views
from main.controllers import player_views, team_views, staff_views

app_name = "main"

main_urlpatterns = [
    path("", main_views.main, name="main"),
]

players_urlpatterns = [
    path("",
         player_views.PlayersListView.as_view(),
         name="players"),
    path(
        "create/",
        player_views.PlayerIDCreateView.as_view(),
        name="player_create",
    ),
    path(
        "<int:pk>/",
        player_views.PlayerIdView.as_view(),
        name="player_id",
    ),
    path(
        "<int:pk>/edit/",
        player_views.PlayerIDEditView.as_view(),
        name="player_id_edit",
    ),
    path(
        "<int:pk>/delete/",
        player_views.PlayerIDDeleteView.as_view(),
        name="player_id_delete",
    ),
    path(
        "deleted/",
        player_views.player_id_deleted,
        name="player_id_deleted",
    ),
]

teams_urlpatterns = [
    path("",
         team_views.TeamListView.as_view(),
         name="teams"),
    path(
        "create/",
        team_views.CreateTeamView.as_view(),
        name="team_create",
    ),
    path(
        "<int:team_id>/",
        team_views.TeamIdView.as_view(),
        name="teams_id",
    ),
    path(
        "<int:team_id>/edit/",
        team_views.UpdateTeamView.as_view(),
        name="team_update",
    ),
    path(
        "<int:team_id>/delete/",
        team_views.DeleteTeamView.as_view(),
        name="team_delete",
    ),
    path(
        "teams/<int:team_id>/",
        team_views.TeamIdView.as_view(),
        name="teams_id",
    ),
]

staffs_urlpatterns = [
    path(
        "",
        staff_views.StaffMemberListView.as_view(),
        name="staffs",
    ),
    path(
        "create/",
        staff_views.StaffMemberIdCreateView.as_view(),
        name="staff_create",
    ),
    path(
        "<int:pk>/",
        staff_views.StaffMemberIdView.as_view(),
        name="staff_id",
    ),
    path(
        "<int:pk>/edit/",
        staff_views.StaffMemberIdEditView.as_view(),
        name="staff_id_edit",
    ),
    path(
        "<int:pk>/delete/",
        staff_views.StaffMemberIdDeleteView.as_view(),
        name="staff_id_delete",
    ),
]

unloads_urlpattern = [
    path("", main_views.unloads, name="unloads"),
]

urlpatterns = [
    path('', include(main_urlpatterns)),
    path('players/', include(players_urlpatterns)),
    path('teams/', include(teams_urlpatterns)),
    path('staffs/', include(staffs_urlpatterns)),
    path('unloads/', include(unloads_urlpattern))
]
