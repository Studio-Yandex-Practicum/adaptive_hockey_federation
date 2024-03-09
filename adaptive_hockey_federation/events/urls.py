from django.urls import include, path
from events import views

app_name = "events"

competitions_urlpatterns = [
    path("", views.EventListView.as_view(), name="competitions"),
    path(
        "create/",
        views.CreateEventView.as_view(),
        name="competition_add",
    ),
    path(
        "<int:pk>/edit/",
        views.UpdateEventView.as_view(),
        name="competition_update",
    ),
    path(
        "<int:pk>/delete/",
        views.DeleteEventView.as_view(),
        name="competition_delete",
    ),
    path(
        "<int:pk>/",
        views.event_team_manage_view,
        name="competitions_id",
    ),
    path(
        "<int:event_id>/teams/<int:pk>/delete/",
        views.DeleteTeamFromEvent.as_view(),
        name="competitions_id_delete",
    ),
    path(
        "competitions/<int:event_id>/teams/<int:pk>/add",
        views.AddTeamToEvent.as_view(),
        name="competitions_id_add",
    ),
]

urlpatterns = [
    path("competitions/", include(competitions_urlpatterns)),
]
