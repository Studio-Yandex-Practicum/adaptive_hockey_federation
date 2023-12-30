from django.urls import path
from users.views import UpdateUserView, UsersListView, DeleteUserView

app_name = 'users'

urlpatterns = [
    path(
        'users/',
        UsersListView.as_view(),
        name='list'
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
    )
]
