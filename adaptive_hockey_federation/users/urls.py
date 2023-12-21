from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import UsersListView

app_name = 'users'

urlpatterns = [
    path(
        'auth/logout/',
        LogoutView.as_view(
            template_name='users/logged_out.html'),
        name='logout'),
    path(
        'auth/login/',
        LoginView.as_view(
            template_name='users/login.html'),
        name='login'),
    path(
        'users/',
        UsersListView.as_view(),
        name='list'
    )
]
