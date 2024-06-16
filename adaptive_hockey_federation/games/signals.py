from django.db.models.signals import post_save
from django.dispatch import receiver
from games.models import Game, GamePlayer, GameTeam
from main.models import Player, Team


@receiver(post_save, sender=Game, dispatch_uid="unique_signal")
def create_game_teams(sender, instance, created, **kwargs):
    """
    Сигнал для автоматического создания GameTeam при создании Game.

    Для последующего использования сигнала при обновлении объекта Game
    реализовано удаление старых GameTeam, которые ссылались на этот Game.
    """
    teams = instance.teams
    queryset_teams = list(
        map(lambda x: Team.objects.get(id=x), teams),
    )
    GameTeam.objects.filter(game=instance).delete()
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
                number=player.number,
                game_team=instance,
            )
            all_players.append(game_player)
        GamePlayer.objects.bulk_create(all_players)
