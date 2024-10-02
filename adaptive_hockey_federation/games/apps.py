from django.apps import AppConfig


class GamesConfig(AppConfig):
    """Класс-конфигуратор для приложения games."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "games"
    verbose_name = "Игры"

    def ready(self) -> None:
        """Импортирование сигналов для приложения."""
        import games.signals  # noqa

        return super().ready()
