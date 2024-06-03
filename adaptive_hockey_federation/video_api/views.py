from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from games.models import Game
from main.models import Player
from video_api.serializers import GameSerializer, PlayerSerializer


@swagger_auto_schema(method="post", request_body=PlayerSerializer)
@api_view(["POST"])
def send_data_player(request):
    """Обработка POST-запроса для создания нового игрока."""
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    responses={200: PlayerSerializer(many=True)},
)
@api_view(["GET"])
def receiving_data_player(request, pk=None):
    """Обработка GET-запроса для получения данных игрока."""
    if pk is not None:
        try:
            player = Player.objects.get(pk=pk)
        except Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlayerSerializer(player)
    else:
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)

    return Response(serializer.data)


@swagger_auto_schema(method="post", request_body=GameSerializer)
@api_view(["POST"])
def send_data_game(request):
    """Обработка POST-запроса для создания новой игры."""
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="get", responses={200: GameSerializer(many=True)})
@api_view(["GET"])
def receiving_data_game(request, pk=None):
    """Обработка GET-запроса для получения данных игры."""
    if pk is not None:
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(game)
    else:
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)

    return Response(serializer.data)
