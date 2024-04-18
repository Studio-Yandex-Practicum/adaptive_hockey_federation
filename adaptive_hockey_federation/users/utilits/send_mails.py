import logging
import os
import sys

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


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def send_welcome_mail(
    team: Team,
    competition: Competition,
    curator_email: str,
) -> None:
    """
    Отправка пригласительного письма
    """
    template = "emailing/welcome_letter.html"
    link = reverse(
        "competitions:competition_id", kwargs={"pk": competition.pk}
    )
    try:
        email = render_email_message(
            subject="Пригласительное письмо",
            context={
                "instance": team,
                "competition": competition,
                "link_to_info": f"http://{os.environ.get('HOST', '127.0.0.1')}:"  # noqa
                f"{os.environ.get('PORT', '8000')}{link}",
            },
            from_email=dev_settings.EMAIL_HOST_USER,
            to=[
                curator_email,
            ],
            template=template,
        )
        email.send(fail_silently=False)
        logger.info(
            f"Электронное письмо успешно отправлено на адрес {curator_email}"
        )
    except Exception as e:
        logger.error(
            "Произошла ошибка при отправке электронного письма"
            f" на {curator_email}: {e}"
        )
