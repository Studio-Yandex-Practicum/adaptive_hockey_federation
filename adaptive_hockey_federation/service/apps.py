from django.apps import AppConfig


class ServiceConfig(AppConfig):
    """Конфигурация приложения Video API."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "service"
