from django.urls import include, path
from events import views

app_name = "events"


competitions_urlpatterns = [
    path("", views.EventListView.as_view(), name="competitions"),
    path(
        "<int:pk>/edit",
        views.UpdateEventView.as_view(),
        name="competition_update",
    ),
    path(
        "<int:pk>/delete",
        views.DeleteEventView.as_view(),
        name="competition_delete",
    ),
    path(
        "<int:pk>/",
        views.TeamsOnEvent.as_view(),
        name="competitions_id",
    ),
    path(
        "<int:event_id>/teams/<int:pk>/delete",
        views.DeleteTeamFromEvent.as_view(),
        name="competitions_id_delete",
    ),
]

urlpatterns = [
    path('competitions/', include(competitions_urlpatterns)),
]
