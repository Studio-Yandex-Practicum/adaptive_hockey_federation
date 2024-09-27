import logging
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
