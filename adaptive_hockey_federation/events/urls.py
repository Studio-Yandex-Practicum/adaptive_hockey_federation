from django.urls import path
from events import views

app_name = "events"


urlpatterns = [
    path("competitions/", views.EventListView.as_view(), name="competitions"),
    path(
        "competitions/<int:pk>/",
        views.TeamsOnEvent.as_view(), name="competitions_id"
    ),
]
