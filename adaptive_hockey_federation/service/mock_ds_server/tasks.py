import random
from time import sleep

from celery.utils.log import get_task_logger

from core.celery import app
from .constants import DELAY, FRAMES_QUANTITY, MAX_FRAMES, MIN_FRAMES

logger = get_task_logger(__name__)


@app.task()
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
