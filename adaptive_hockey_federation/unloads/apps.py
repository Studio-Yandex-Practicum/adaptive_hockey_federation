from django.apps import AppConfig


class UnloadsConfig(AppConfig):
    """Класс-конфигуратор для приложения unloads."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "unloads"
    verbose_name = "Выгрузки"
