import os
from typing import Any
from urllib.parse import urljoin

import environ
import requests
from rest_framework import status


env = environ.Env()


def send_request_to_video_processing_service(
    path: str,
    request_data: dict[str, Any],
    base_url: str = os.getenv(
        "PROCESSING_SERVICE_BACE_URL",
        "http://127.0.0.1:8010/",
    ),
    http_method: str = "post",
    **kwargs: dict[Any, Any],
) -> status:
    """
    Отправка запросов к эндпоинтам сервиса по обработке видео с играми.

    Обрабатывает все поддерживаемые http методы библиотекой requests.
    Формируется конечный адрес base_url + path, куда будет отправлен запрос,
    В аргументе request_data передается словарь,
    содержащий имя аргмуента и значение требуемые
    сигатурой соответствующего http метода.
    """
    endpoint = urljoin(base_url, path)

    if hasattr(requests, http_method.lower()):
        response = getattr(requests, http_method)(
            endpoint,
            **request_data,
            **kwargs,
        )
        return response.status_code
    raise AttributeError(f"Http метод: {http_method} не обслуживается")
