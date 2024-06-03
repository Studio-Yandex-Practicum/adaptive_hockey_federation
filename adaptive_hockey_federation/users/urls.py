from django.urls import include, path

from users.views import (
    CreateUserView,
    DeleteUserView,
    PasswordSetView,
    UpdateUserView,
    UsersListView,
)

app_name = "users"

users_urlpatterns = [
    path(
        "",
        UsersListView.as_view(),
        name="users",
    ),
    path(
        "create/",
        CreateUserView.as_view(),
        name="user_create",
    ),
    path(
        "<int:pk>/edit/",
        UpdateUserView.as_view(),
        name="user_update",
    ),
    path(
        "<int:pk>/delete/",
        DeleteUserView.as_view(),
        name="user_delete",
    ),
    path(
        "set_password/<uidb64>/<token>/",
        PasswordSetView.as_view(),
        name="password_set",
    ),
]

urlpatterns = [
    path("users/", include(users_urlpatterns)),
]
