from games.models import Game
from rest_framework import generics
from video_api.serializers import GameFeatureSerializer
from service.a_hockey_requests import send_request_to_video_processing_service


class VideoRecognitionView(generics.RetrieveAPIView):
    """Отправка запроса на эндпоинт /process для обработки видео с игрой."""

    queryset = Game.objects.all()
    serializer_class = GameFeatureSerializer

    def get(self, request, *args, **kwargs):
        """Переопределяем метод для отправки запросов к серсиву."""
        response = self.retrieve(request, *args, **kwargs)
        service_status = send_request_to_video_processing_service(
            "/process",
            response.data,
        )
        # Временно эллипсис, что бы линтеры пропускали.
        # TODO дописать логику когда будет докручен сервис по обработке видео
        if service_status != 200:
            pass
        return response
