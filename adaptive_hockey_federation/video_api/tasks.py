from core.celery import app
from service.a_hockey_requests import send_request_to_video_processing_service


@app.task
def test_high_priority_task(*args, **kwargs):
    print("Таск с высоким приоритетом")
    path = kwargs.get("path")
    data = kwargs.get("data")
    send_request_to_video_processing_service(path, data)
    return


@app.task
def test_low_priority_task(*args, **kwargs):
    print("Таск с низким приоритетом")
    path = kwargs.get("path")
    data = kwargs.get("data")
    send_request_to_video_processing_service(path, data)
    return
