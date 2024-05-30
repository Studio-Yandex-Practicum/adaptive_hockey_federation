from django.urls import include, path
from games import views

app_name = "games"

games_urlpattern = [
    path("", views.GamesListView.as_view(), name="games"),
    path("create/", views.GameCreateView.as_view(), name="game_create"),
    path(
        "<int:game_id>/edit/",
        views.GameEditView.as_view(),
        name="game_edit",
    ),
]

urlpatterns = [
    path("games/", include(games_urlpattern)),
]
