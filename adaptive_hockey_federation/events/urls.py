from django.urls import path
from events import views

app_name = "events"

urlpatterns = [
    path("competitions/", views.EventListView.as_view(), name="competitions"),
    path(
        "competitions/create/",
        views.CreateEventView.as_view(),
        name="competition_add",
    ),
    path(
        "competitions/<int:pk>/edit",
        views.UpdateEventView.as_view(),
        name="competition_update",
    ),
    path(
        "competitions/<int:pk>/delete",
        views.DeleteEventView.as_view(),
        name="competition_delete",
    ),
    path(
        "competitions/<int:pk>/",
        views.event_team_manage_view,
        name="competitions_id",
    ),
    path(
        "competitions/<int:event_id>/teams/<int:pk>/delete",
        views.DeleteTeamFromEvent.as_view(),
        name="competitions_id_delete",
    ),
    path(
        "competitions/<int:event_id>/teams/<int:pk>/add",
        views.AddTeamToEvent.as_view(),
        name="competitions_id_add",
    ),
]
