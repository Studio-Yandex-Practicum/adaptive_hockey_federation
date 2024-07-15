from typing import Any
from urllib.parse import urljoin

import requests
from django.conf import settings


def send_request_to_video_processing_service(
    path: str,
    request_data: dict[str, Any],
    base_url: str = settings.PROCESSING_SERVICE_BASE_URL,
    http_method: str = "post",
    **kwargs: dict[Any, Any],
) -> requests.Response:
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
        return response
    raise AttributeError(f"Http метод: {http_method} не обслуживается")
