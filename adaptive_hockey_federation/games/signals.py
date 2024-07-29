from pathlib import Path
import json
import random

from django.db.models.signals import post_save
from django.dispatch import receiver
from games.models import Game, GamePlayer, GameTeam
from main.models import Player, Team
from video_api.tasks import get_player_video_frames


@receiver(post_save, sender=Game, dispatch_uid="unique_signal")
def create_game_teams(sender, instance, created, **kwargs):
    """
    Сигнал для автоматического создания GameTeam при создании Game.

    Для последующего использования сигнала при обновлении объекта Game
    реализовано удаление старых GameTeam, которые ссылались на этот Game.
    """
    teams = instance.competition.teams.all()
    queryset_teams = list(
        map(lambda x: Team.objects.get(id=x.id), teams),
    )
    GameTeam.objects.filter(game=instance).delete()
    queryset_teams = random.sample(queryset_teams, 2)
    for team in queryset_teams:
        game_team = GameTeam(
            id=team.id,
            name=team.name,
            discipline_name=team.discipline_name.name,
            game=instance,
        )
        game_team.players = Player.objects.filter(
            team=team,
        )
        game_team.save()

    # Моковая реализация запуска воркера по отправке запроса на
    # обработку видео и сохранение фреймов игрока в бд
    # TODO для реального запроса к дс-ам данные запрашиваются в бд,
    # сериализуются и оптравляются в воркер
    # TODO необходимо пересмотреть логику создания объекта игры,
    # конкретно изменение
    # номеров игроков. Оно должно происходить до того
    # как объект игры попадёт в бд.
    if created:
        # пример тестовых данных для запроса берется из сервиса дс-ов
        test_data = (
            Path(__file__).resolve().parent.parent.parent
            / "a_hockey-main/app/src/test/test_query_process.json"
        )

        with open(test_data, "r") as file:
            data_from_json = json.load(file)
            request_data = {"json": data_from_json}

        get_player_video_frames.apply_async(
            args=["/process", request_data],
            queue="process_queue",
            priority=255,
        )


@receiver(post_save, sender=GameTeam, dispatch_uid="unique_signal")
def create_game_players(sender, instance, created, **kwargs):
    """Сигнал для автоматического создания GamePlayer при создании GameTeam."""
    if created:
        queryset_players = instance.players
        all_players = []
        for player in queryset_players:
            game_player = GamePlayer(
                id=player.id,
                name=player.name,
                last_name=player.surname,
                patronymic=player.patronymic,
                number=player.number,
                game_team=instance,
            )
            all_players.append(game_player)
        GamePlayer.objects.bulk_create(all_players)
