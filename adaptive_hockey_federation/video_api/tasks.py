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
from users.utilits.send_mails import send_info_mail
from .serializers import GameDataPlayerSerializerMock


logger = logging.getLogger(__name__)


@app.task(base=Singleton)
def get_player_video_frames(*args, **kwargs):
    """Таск для запуска обработки видео."""
    logger.info("Добавлен новый объект игры, запускаем воркер")
    return send_request_to_process_video(kwargs["data"])


@app.task()
def create_player_video(
    *args,
    **kwargs,
):
    """Таск для нарезки видео с моментами игрока."""
    # Мок реализация фреймов для нарезки видео с моментами игрока.
    # Пока подставляются тестовые фреймы.
    # TODO удалить мок реализацию, как в бд появятся фреймы по игрокам.

    input_file = kwargs["input_file"]
    output_file = kwargs["output_file"]
    # player = kwargs["player"]
    # game = kwargs["game"]
    frames = kwargs["frames"]
    if os.path.exists(output_file):
        return

    slicing_video_with_player_frames(input_file, output_file, frames)
    return f"Видео обработано. {args}"


def bulk_create_gamedataplayer_objects(sender=None, **kwargs):
    """
    Сохранение параметров видео игроков от сервера DS.

    Вызов таски нарезки видео.
    """
    result = kwargs.get("result")
    task_params = sender.request.kwargs["data"]
    user_email = sender.request.kwargs["user_email"]

    # TODO уточнить структуру ответа DS
    serializer = GameDataPlayerSerializerMock(data=result, many=True)
    if serializer.is_valid():
        object_data = serializer.validated_data
        game = Game.objects.get(pk=task_params["game_id"])
        gamedata_players_to_create = []
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
                gamedata_players_to_create.append(
                    GameDataPlayer(
                        player=player,
                        game=game,
                        data=json.dumps(track),
                    )
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
                # TODO заменить название исходного файла
                # видео с игрой нужно скачать
                # ссылка на видео с игрой task_params["game_link"]
                input_file = "input_file.mp4"
                output_file = (
                    f"video_game_{task_params['game_id']}_"
                    f"player_{game_player.id}.mp4"
                )
                create_player_video.apply_async(
                    args=["Обработка с низким приоритетом"],
                    kwargs={
                        "input_file": input_file,
                        "output_file": output_file,
                        "player": str(player),
                        "game": game.name,
                        "user_email": user_email,
                        "frames": track["frames"],
                        "priority": 255,
                    },
                )
        if gamedata_players_to_create:
            GameDataPlayer.objects.bulk_create(gamedata_players_to_create)
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


def send_success_mail(sender=None, **kwargs):
    """Вызывает функцию отправки письма о готовности видео с игроком."""
    player = sender.request.kwargs["player"]
    game = sender.request.kwargs["game"]
    user_email = sender.request.kwargs["user_email"]
    send_info_mail(
        "Обработка видео завершена",
        f'Завершена обработка видео игрока {player} в игре "{game}".',
        user_email,
    )


@worker_process_init.connect
def mail_success_video_process(**kwargs):
    """Обработка сигнала task_success таски create_player_video."""
    task_success.connect(
        send_success_mail,
        sender=current_app.tasks[create_player_video.name],
    )
