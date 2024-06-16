from competitions import views
from django.urls import include, path

app_name = "competitions"

competitions_urlpatterns = [
    path("", views.CompetitionListView.as_view(), name="competitions"),
    path(
        "create/",
        views.CreateCompetitionView.as_view(),
        name="competition_add",
    ),
    path(
        "<int:pk>/edit/",
        views.UpdateCompetitionView.as_view(),
        name="competition_update",
    ),
    path(
        "<int:pk>/delete/",
        views.DeleteCompetitionView.as_view(),
        name="competition_delete",
    ),
    path(
        "<int:pk>/",
        views.competition_team_manage_view,
        name="competition_id",
    ),
    path(
        "<int:competition_id>/teams/<int:pk>/delete/",
        views.DeleteTeamFromCompetition.as_view(),
        name="competitions_id_delete",
    ),
    path(
        "<int:competition_id>/teams/<int:pk>/add/",
        views.AddTeamToCompetition.as_view(),
        name="competitions_id_add",
    ),
]

urlpatterns = [
    path("competitions/", include(competitions_urlpatterns)),
]
