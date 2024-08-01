import logging
import sys

import yadisk
from django.conf import settings
from yadisk.exceptions import (
    ForbiddenError,
    PathNotFoundError,
    ResourceIsLockedError,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def download_file(video_link: str, media_data_path: str) -> str | None:
    """Скачать файл с Yandex Disk."""
    error_message: str | None = None
    client = yadisk.Client(token=settings.YANDEX_DISK_OAUTH_TOKEN)

    with client:
        if not client.check_token():
            error_message = "Токен Yandex Disk недействителен."
            logger.exception(error_message)
            return error_message

        try:
            client.download_by_link(video_link, media_data_path)
        except PathNotFoundError:
            error_message = f"Файл {video_link} не найден на Yandex Disk."
            logger.exception(error_message)
        except ForbiddenError:
            error_message = "Не хватает прав, чтобы выполнить запрос."
            logger.exception(error_message)
        except ResourceIsLockedError:
            error_message = f"Файл {video_link} заблокирован другой операцией."
            logger.exception(error_message)
        except Exception as error:
            logger.exception("Error")
            return str(error)
        return error_message
