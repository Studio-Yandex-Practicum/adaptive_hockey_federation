from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Класс-конфигуратор для приложения users."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"
