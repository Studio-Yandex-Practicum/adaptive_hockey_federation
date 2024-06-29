import time

from celery_singleton import Singleton
from core.celery import app
from service.a_hockey_requests import send_request_to_video_processing_service
from service.video_processing import slicing_video_with_player_frames


@app.task(base=Singleton)
def get_player_video_frames(*args, **kwargs):
    time.sleep(10)
    path, data = kwargs.get("path"), kwargs.get("data")
    response = send_request_to_video_processing_service(path, data)
    return response.content


@app.task(base=Singleton)
def create_player_video(*args, **kwargs):
    # TODO моковая реализация, должно передаваться данные
    # необходимые для нарезки видео с игроком
    input_file = kwargs.get("input_file")
    output_file = kwargs.get("output_file")
    frames = kwargs.get("frames")
    slicing_video_with_player_frames(input_file, output_file, frames)
