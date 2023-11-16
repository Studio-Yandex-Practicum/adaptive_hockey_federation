from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path

app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login',
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(),
        name='password_reset'),
]
