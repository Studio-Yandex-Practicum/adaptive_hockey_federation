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


def download_file(video_link, media_data_path):
    """Скачать файл с Yandex Disk."""
    client = yadisk.Client(token=settings.YANDEX_DISK_OAUTH_TOKEN)

    with client:
        if not client.check_token():
            error = "Токен Yandex Disk недействителен."
            logger.exception(error)
            return error

        try:
            client.download_by_link(video_link, media_data_path)
        except PathNotFoundError:
            error = f"Файл {video_link} не найден на Yandex Disk."
            logger.exception(error)
            return error
        except ForbiddenError:
            error = "Не хватает прав, чтобы выполнить запрос."
            logger.exception(error)
            return error
        except ResourceIsLockedError:
            error = f"Файл {video_link} заблокирован другой операцией."
            logger.exception(error)
            return error
        except Exception as error:
            logger.exception("Error")
            return error
