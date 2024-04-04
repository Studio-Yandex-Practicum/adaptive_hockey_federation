import os

from competitions.models import Competition
from core.config import dev_settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from main.models import Team
from users.models import User
from users.utilits.render import render_email_message


def send_password_reset_email(
    instance: User,
    message: str | None = None,
    template: str | None = None,
) -> None:
    """
    Отправка письма с ссылкой восстановления пароля
    """
    if template is None:
        template = "emailing/password_reset_email.html"
    reset_link = get_password_reset_link(instance)
    email = render_email_message(
        subject="Доступ к аккаунту пользователя",
        context={
            "password_reset_link": reset_link,
            "message": message,
            "user": instance,
        },
        from_email=dev_settings.EMAIL_HOST_USER,
        to=[
            instance.email,
        ],
        template=template,
    )
    email.send(fail_silently=False)


def get_password_reset_link(instance: User) -> str:
    """
    Функция генерации ссылки для смены пароля
    """
    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    token = default_token_generator.make_token(instance)
    reset_url = reverse("users:password_set", args=[uid, token])
    return (
        f"http://{os.environ.get('HOST', '127.0.0.1')}:"
        f"{os.environ.get('PORT', '8000')}{reset_url}"
    )


def send_welcome_mail(
        team: Team,
        competition: Competition,
        email: str,
) -> None:
    """
    Отправка пригласительного письма
    """
    template = "emailing/welcome_letter.html"
    link = reverse(
        "competitions:competitions_id",
        kwargs={"pk": competition.pk}
    )
    email = render_email_message(
        subject="Пригласительное письмо",
        context={
            "instance": team,
            "competition": competition,
            "link_to_info":
                f"http://{os.environ.get('HOST', '127.0.0.1')}:"
                f"{os.environ.get('PORT', '8000')}{link}"},
        from_email=dev_settings.EMAIL_HOST_USER,
        to=[
            email,
        ],
        template=template,
    )
    email.send(fail_silently=False)
