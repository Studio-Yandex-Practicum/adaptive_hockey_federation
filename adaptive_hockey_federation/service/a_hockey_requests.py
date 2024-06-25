import os
import random
import string
from typing import Any
from urllib.parse import urljoin

import requests
from rest_framework import status
from django.conf import settings


def send_request_to_video_processing_service(
    path: str,
    request_data: dict[str, Any],
    base_url: str = settings.PROCESSING_SERVICE_BASE_URL,
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
        content = response.content
        save_directory = os.path.join(
            os.path.dirname(__file__),
            "test_response/",
        )
        random_name = (
            "".join(
                [
                    string.ascii_lowercase[idx]
                    for idx in range(random.randint(5, 10))  # noqa: COM812
                ],
            )
            + ".mp4"
        )
        full_save_dir = os.path.join(save_directory, random_name)
        print(random_name)
        with open(full_save_dir, "wb") as video:
            video.write(content)
        return response.status_code
    raise AttributeError(f"Http метод: {http_method} не обслуживается")
