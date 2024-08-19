import json
import logging
import os

from celery import current_app
from celery.signals import task_success, worker_process_init
from celery_singleton import Singleton
from django.db import transaction

from core.celery import app
from games.models import Game, GameDataPlayer, GamePlayer
from main.models import Player
from service.a_hockey_requests import send_request_to_process_video
from service.video_processing import slicing_video_with_player_frames
from .serializers import GameDataPlayerSerializerMock


logger = logging.getLogger(__name__)


@app.task(base=Singleton)
def get_player_video_frames(*args, **kwargs):
    """Таск для запуска обработки видео."""
    logger.info("Добавлен новый объект игры, запускаем воркер")
    return send_request_to_process_video(kwargs["data"])


@app.task()
def create_player_video(
    input_file,
    output_file,
    player_id,
    game_id,
    *args,
    **kwargs,
):
    """Таск для нарезки видео с моментами игрока."""
    # Мок реализация фреймов для нарезки видео с моментами игрока.
    # Пока подставляются тестовые фреймы.
    # TODO удалить мок реализацию, как в бд появятся фреймы по игрокам.

    if os.path.exists(output_file):
        return

    frames = [i for i in range(15000, 15430, 5)]
    # frames = GameDataPlayer.objects.filter(
    #     player_id=player_id, game_id=game_id
    # ).first().data

    slicing_video_with_player_frames(input_file, output_file, frames)
    return f"Видео обработано. {args}"


def bulk_create_gamedataplayer_objects(sender=None, **kwargs):
    """
    Сохранение параметров видео игроков от сервера DS.

    Вызов таски нарезки видео.
    """
    result = kwargs.get("result")
    task_params = sender.request.kwargs["data"]

    # TODO уточнить структуру ответа DS
    serializer = GameDataPlayerSerializerMock(data=result, many=True)
    if serializer.is_valid():
        object_data = serializer.validated_data
        game = Game.objects.get(pk=task_params["game_id"])
        with transaction.atomic():
            for track in object_data:
                try:
                    game_player = GamePlayer.objects.get(
                        game_team__game=game,
                        game_team_id=track["team"],
                        number=track["number"],
                    )
                except GamePlayer.DoesNotExist:
                    logger.warning(
                        f"Игрок с номером {track['number']} "
                        f"команды {track['team']} "
                        f"в игре {task_params['game_id']} не найден.",
                    )
                    continue
                except GamePlayer.MultipleObjectsReturned:
                    logger.warning(
                        f"В команде {track['team']} "
                        f"несколько игроков с номером {track['number']} "
                        f"участвовало в игре {task_params['game_id']}.",
                    )
                    continue
                player = Player.objects.get(pk=game_player.id)
                # TODO возможно следует использовать bulk_create
                GameDataPlayer.objects.update_or_create(
                    player=player,
                    game=game,
                    defaults={"data": json.dumps(track)},
                )
                logger.info(
                    (
                        f"Cоздаем видео для игрока "
                        f"{player.get_name_and_position()}"
                    ),
                )
                # TODO в args передают аргументы
                # нужные для нарезки видео с игроком
                # create_player_video(
                create_player_video.apply_async(
                    args=["Обработка с низким приоритетом"],
                    kwargs={
                        "frames": track["frames"],
                        "priority": 255,
                    },
                )
    else:
        logger.error(serializer.errors)


@worker_process_init.connect
def on_pool_process_init(**kwargs):
    # Что бы отрабатывал сигнал task_success
    # https://github.com/celery/celery/issues/2343
    # https://django.fun/docs/celery/5.1/userguide/signals/#worker-process-init
    task_success.connect(
        bulk_create_gamedataplayer_objects,
        sender=current_app.tasks[get_player_video_frames.name],
    )


# TODO оправить письмо при завершении обработки видео
# @worker_process_init.connect
# def mail_success_video_process(**kwargs):
#     task_success.connect(
#         create_player_video,
#         sender=current_app.tasks[],
#     )
