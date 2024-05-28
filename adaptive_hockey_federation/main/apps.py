from django.apps import AppConfig


class MainConfig(AppConfig):
    """Класс-конфигуратор для приложения main."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    verbose_name = "БД игроков и команд"
