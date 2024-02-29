from django.urls import path
from users.views import (
    CreateUserView,
    DeleteUserView,
    PasswordSetView,
    UpdateUserView,
    UsersListView,
)

app_name = 'users'

urlpatterns = [
    path(
        'users/',
        UsersListView.as_view(),
        name='users'
    ),
    path(
        'user_update/<int:pk>/',
        UpdateUserView.as_view(),
        name='user_update'
    ),
    path(
        'user_delete/<int:pk>/',
        DeleteUserView.as_view(),
        name='user_delete'
    ),
    path(
        'user_create/',
        CreateUserView.as_view(),
        name='user_create'
    ),
    path(
        "set_password/<uidb64>/<token>/",
        PasswordSetView.as_view(),
        name="password_set",
    ),
]
