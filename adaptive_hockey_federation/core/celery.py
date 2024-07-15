import os

from celery import Celery
from kombu import Queue
from .config.base_settings import env, BASE_DIR


env_dir = os.path.join(BASE_DIR.parent, ".env")
env.read_env(env_dir)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"core.config.{env('SETTINGS_LEVEL', default='dev')}_settings",
)

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.broker_transport_options = {
    "queue_order_strategy": "priority",
}

app.conf.task_queues = (
    Queue("process_queue"),
    Queue("slice_player_video_queue"),
)
