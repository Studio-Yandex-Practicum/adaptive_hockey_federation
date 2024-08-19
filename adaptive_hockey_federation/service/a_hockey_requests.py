import logging
from typing import Any
from urllib.parse import urljoin

import requests
from django.conf import settings
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def check_api_health_status() -> None:
    """
    Отправка запроса на эндпоинт /health для проверки состояния сервиса.

    :raises RequestException: Если возникла ошибка.
    """
    try:
        response = requests.get(
            urljoin(settings.PROCESSING_SERVICE_BASE_URL, "/health"),
        )
        response.raise_for_status()
    except RequestException as error:
        raise RequestException(
            f"Сервис по обработке видео недоступен: {error}",
        ) from error


def send_request_to_process_video(
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Отправка запроса к эндпоинту /process для обработки видео.

    :param data: Словарь с данными для обработки видео.
    :returns: Результат обработки видео.
    :raises RequestException: Если возникла ошибка при обработке видео.
    """
    logger.info("Отправка запроса к серверу DS.")
    try:
        response = requests.post(
            urljoin(settings.PROCESSING_SERVICE_BASE_URL, "/process"),
            json=data,
            timeout=(0.5, None),
        )
        return response.json()
    except RequestException as error:
        logger.error(f"Ошибка подключения к серверу распознавания: {error}")
        return {
            "message": "Возникла ошибка при попытке обработать видео: "
            "Ошибка подключения к серверу распознавания.",
        }
