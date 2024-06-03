from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import gettext_lazy as _

from core.constants import Directory, MainConstantsInt
from users.models import User


class Unload(models.Model):
    """Выгрузка."""

    unload_name = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
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
        verbose_name=_("Ссылка на файл"),
        upload_to=Directory.UNLOAD_DIR + "/",
    )

    class Meta:
        verbose_name = "Выгрузку"
        verbose_name_plural = "Выгрузки"
        ordering = ("date",)
        permissions = [
            ("list_view_unload", "Can view list of Выгрузку"),
        ]

    def __str__(self) -> str:
        """Метод, использующий unload_name для строкового представления."""
        return f"{self.unload_name}"


@receiver(post_delete, sender=Unload)
def document_file_delete(sender, instance, **kwargs):
    if instance.unload_file_slug:
        instance.unload_file_slug.delete(False)
