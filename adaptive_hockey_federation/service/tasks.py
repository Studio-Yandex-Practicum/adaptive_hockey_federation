import json
import os
from time import sleep

from celery.signals import worker_process_init, task_success
from celery.utils.log import get_task_logger
from fastapi.responses import JSONResponse

from core.celery import app


logger = get_task_logger(__name__)

DELAY = 5 * 60 * 60  # in seconds


@app.task()
def mock_ds_process() -> JSONResponse:
    logger.info("Start mock_ds_process")
    sleep(DELAY)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    test_response_file = os.path.join(
        current_directory,
        "test_response.json.txt",
    )
    with open(test_response_file, "r") as file:
        response = json.load(file)
    logger.info("End mock_ds_process")
    return response


@worker_process_init.connect
def on_pool_process_init(**kwargs):
    task_success.connect()
