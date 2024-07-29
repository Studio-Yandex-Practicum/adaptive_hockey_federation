from requests.exceptions import RequestException

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from games.models import Game
from service.a_hockey_requests import (
    check_api_health_status,
    send_request_to_process_video,
)
from video_api.serializers import GameFeatureSerializer


class VideoRecognitionView(APIView):
    """Представление для обработки видео."""

    def post(self, request, *args, **kwargs):
        """Отправка запроса к сервису по обработке видео."""
        try:
            check_api_health_status()

            game = get_object_or_404(Game, id=kwargs.get("pk"))
            serializer = GameFeatureSerializer(game)

            response = send_request_to_process_video(serializer.data)
            return Response(response, status=status.HTTP_200_OK)
        except RequestException as error:
            raise APIException(
                str(error),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
