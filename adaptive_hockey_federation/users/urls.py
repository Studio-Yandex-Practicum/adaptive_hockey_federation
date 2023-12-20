from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(
            template_name='users/logged_out.html'),
        name='logout'),
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html'),
        name='login'),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'),
        name='password_reset_form'),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'),
        name='password_change_form'),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'),
        name='password_change_done_form'),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
]
