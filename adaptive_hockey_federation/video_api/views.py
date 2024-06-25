from games.models import Game
from rest_framework import generics
from video_api.serializers import GameFeatureSerializer
from .tasks import test_high_priority_task, test_low_priority_task


class VideoRecognitionView(generics.RetrieveAPIView):
    """Отправка запроса на эндпоинт /process для обработки видео с игрой."""

    queryset = Game.objects.all()
    serializer_class = GameFeatureSerializer

    def get(self, request, *args, **kwargs):
        """Переопределяем метод для отправки запросов к серсиву."""
        response = self.retrieve(request, *args, **kwargs)
        request_data_to_service = {"json": response.data}

        # Задачи выполняются: low, high, high, low. Первая low т.к.
        # первая инициализируется и попадает в очередь
        # Во время выполнения первого таска, остальные
        # инициализируются и выполняются уже в соответсвии с
        # приоритетом

        low_task = test_low_priority_task.s(
            path="/process",
            data=request_data_to_service,
        )
        high_task = test_high_priority_task.s(
            path="/process",
            data=request_data_to_service,
        )
        low_task.apply_async(priority=200)
        low_task.apply_async(priority=200)
        high_task.apply_async(priority=0)
        high_task.apply_async(priority=0)

        return response

        # service_status = send_request_to_video_processing_service(
        #     "/process",
        #     request_data_to_service,
        # )
        # # Временно эллипсис, что бы линтеры пропускали.
        # # TODO дописать логику когда будет докручен сервис по обработке видео
        # if service_status != 200:
        #     pass
        # return response
