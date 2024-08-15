import os

from celery import Celery

from .config.base_settings import env, BASE_DIR


env_dir = os.path.join(BASE_DIR.parent, ".env")
env.read_env(env_dir)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"core.config.{env('SETTINGS_LEVEL', default='dev')}_settings",
)

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

# app.autodiscover_tasks()
# TODO удалить вместе с mock_ds_server
app.autodiscover_tasks(["service.mock_ds_server"])

app.conf.broker_transport_options = {
    "queue_order_strategy": "priority",
}

# TODO может очереди нужны?
# app.conf.task_routes = ([
#     ("video_api.tasks.get_player_video_frames", {"queue": "process_queue"}),
#     (
#         "video_api.tasks.create_player_video",
#         {"queue": "slice_player_video_queue"},
#     ),
# TODO удалить вместе с mock_ds_server
#     ("service.mock_ds_server.tasks.*", {"queue": "mock_ds_server"}),
# ],)
