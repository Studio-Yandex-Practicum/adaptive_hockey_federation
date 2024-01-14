from django.urls import path
from users.views import UsersListView

app_name = 'users'

urlpatterns = [
    path(
        'users/',
        UsersListView.as_view(),
        name='users'
    ),
]
