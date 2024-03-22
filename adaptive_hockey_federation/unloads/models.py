from core.constants import CHAR_FIELD_LENGTH
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Unload(models.Model):
    """Выгрузка."""

    unload_name = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_("Имя выгрузки"),
        default="Выгрузка",
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата выгрузки",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    unload_file_slug = models.FileField(
        verbose_name=_("Ссылка на файл"), upload_to="data/"
    )

    class Meta:
        verbose_name = "Выгрузку"
        verbose_name_plural = "Выгрузки"
        ordering = ("date",)

    def __str__(self) -> str:
        return f"{self.unload_name}"
