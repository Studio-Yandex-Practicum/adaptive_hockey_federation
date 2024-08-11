import json
import logging
import time
from pathlib import Path

from celery import current_app
from celery.signals import task_success, worker_process_init
from celery_singleton import Singleton
from django.db import transaction

from core.celery import app
from games.models import GameDataPlayer
from service.a_hockey_requests import send_request_to_process_video
from service.video_processing import slicing_video_with_player_frames
from .serializers import GameDataPlayerSerializer


logger = logging.getLogger(__name__)


@app.task(base=Singleton)
def get_player_video_frames(*args, **kwargs):
    """Таск для запуска обработки видео."""
    logger.warning("Добавлен новый объект игры, запускаем воркер")
    response = send_request_to_process_video(kwargs.get("data"))
    return response


@app.task()
def create_player_video(*args, **kwargs):
    # TODO моковая реализация, должно передаваться данные
    # необходимые для нарезки видео с игроком
    time.sleep(10)
    args = args[0]
    game_link = "https://disk.yandex.ru/i/JLh__1IbAfmK-Q"
    output_file = (
        Path(__file__).resolve().parent.parent / "service/test_video/test.mp4"
    )
    frames = [i for i in range(15000, 15430, 5)]
    slicing_video_with_player_frames(game_link, output_file, frames)
    return f"Видео обработано. {args}"


def bulk_create_gamedataplayer_objects(sender=None, **kwargs):
    # result - получает результат работы из sender
    result = kwargs.get("result")
    parse_data = json.loads(result)

    serializer = GameDataPlayerSerializer(data=parse_data)
    if serializer.is_valid():
        object_data = serializer.validated_data
        # В тестовом запросе индекс у игры 0, изменить
        # на любой другой индекс игры в бд
        game = object_data["game_id"]
        tracking = object_data["tracking"]
        with transaction.atomic():
            for track in tracking:
                player = track["player_id"]
                del track["player_id"]
                # TODO возможно следует использовать bulk_create
                GameDataPlayer.objects.update_or_create(
                    player=player,
                    game=game,
                    data=json.dumps(track),
                )
                print(
                    (
                        f"Cоздаем видео для игрока "
                        f"{player.get_name_and_position()}"
                    ),
                )
                # TODO в args передают аргументы
                # нужные для нарезки видео с игроком
                create_player_video.apply_async(
                    args=["Обработка с низким приоритетом"],
                    queue="slice_player_video_queue",
                    priority=255,
                )
    print(serializer.errors)
    # Задача ничего не возвращает.
    # Возможно из-за способа её вызова через worker_process_init


@worker_process_init.connect
def on_pool_process_init(**kwargs):
    # Что бы отрабатывал сигнал task_success
    # https://github.com/celery/celery/issues/2343
    # https://django.fun/docs/celery/5.1/userguide/signals/#worker-process-init
    task_success.connect(
        bulk_create_gamedataplayer_objects,
        sender=current_app.tasks[get_player_video_frames.name],
    )
