import logging
import random
from time import sleep

# from celery import Celery  # TODO раскоментировать после добавления celery
# from celery.utils.log import get_task_logger

from constants import DELAY, FRAMES_QUANTITY, MAX_FRAMES, MIN_FRAMES
from adaptive_hockey_federation.core.logging import configure_logging

# app = Celery(__name__)  # TODO раскоментировать после добавления celery
# app.config_from_object("celeryconfig")

logger = logging.getLogger(__name__)

configure_logging()


# @app.task(name="mock_ds_process")  # TODO раскоментировать после добавления celery
def mock_ds_process(*args, **kwargs) -> list[dict[str, int | list[int]]]:
    logger.info("Старт заглушки DS сервера")
    sleep(DELAY)
    teams = zip(
        kwargs["data"]["team_ids"],
        kwargs["data"]["player_numbers"],
        strict=True,
    )
    response = []
    for team, numbers in teams:
        for number in numbers:
            frames = [
                random.randint(MIN_FRAMES, MAX_FRAMES)
                for _ in range(FRAMES_QUANTITY)
            ]
            response.append(
                {
                    "number": number,
                    "team": team,
                    "counter": 0,  # непонятный параметр
                    "frames": sorted(frames),
                },
            )
    logger.info("Завершение заглушки DS сервера")
    return response
