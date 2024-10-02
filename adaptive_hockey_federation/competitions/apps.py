from django.apps import AppConfig


class CompetitionsConfig(AppConfig):
    """Класс-конфигуратор для приложения competitions."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "competitions"
    verbose_name = "Соревнования"
