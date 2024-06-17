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
    base_url: str = os.getenv("URL", "http://127.0.0.1:8010/"),
) -> status:
    """Отправка запросов к эндпоинтам сервиса по обработке видео с играми."""
    endpoint = urljoin(base_url, path)
    response = requests.post(endpoint, json=request_data)
    return response.status_code
