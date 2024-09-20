import os
import logging
import sys
from functools import wraps

import yadisk
from yadisk import Client
from django.conf import settings
from yadisk.exceptions import (
    ForbiddenError,
    PathNotFoundError,
    ResourceIsLockedError,
)

from core.constants import YadiskDirectory


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def yadisk_client(func):
    """
    Декоратор для работы с клиентом Yandex Disk.

    Декорируемая функция должна принимать первым аргументом экземпляр
    `yadisk.Client`.

    Пример использования:
        @yadisk_client
        def function(client, *args, **kwargs):
            pass
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with yadisk.Client(
                token=settings.YANDEX_DISK_OAUTH_TOKEN,
            ) as client:
                return func(client, *args, **kwargs)
        except PathNotFoundError:
            error_message = "Файл не найден на Yandex Disk."
            logger.exception(error_message)
            raise PathNotFoundError(msg=error_message)
        except ForbiddenError:
            error_message = "Не хватает прав, чтобы выполнить запрос."
            logger.exception(error_message)
            raise ForbiddenError(msg=error_message)
        except ResourceIsLockedError:
            error_message = "Файл заблокирован другой операцией."
            logger.exception(error_message)
            raise ResourceIsLockedError(msg=error_message)

    return wrapper


@yadisk_client
def check_file_exists_on_disk(client: Client, file_path: str) -> bool:
    """Проверить существование файла на Yandex Disk."""
    return client.exists(file_path)


@yadisk_client
def download_file_by_link(
    client: Client,
    video_link: str,
    media_data_path: str,
) -> None:
    """Скачать файл с Yandex Disk по ссылке."""
    client.download_public(video_link, media_data_path)


def check_player_game_exists_on_disk(player_game_file_name: str) -> bool:
    """Проверить существование файла с игроком на Yandex Disk."""
    player_game_path_on_disk = os.path.join(
        YadiskDirectory.PLAYER_GAMES,
        player_game_file_name,
    )
    return check_file_exists_on_disk(player_game_path_on_disk)


def download_file_by_link_task(
    video_link: str,
    media_data_path: str,
):
    """Задача для скачивания файла с Yandex Disk."""
    if os.path.exists(media_data_path):
        logger.info(f"Файл {media_data_path} уже скачан на диске.")
        return
    download_file_by_link(
        video_link=video_link,
        media_data_path=media_data_path,
    )
