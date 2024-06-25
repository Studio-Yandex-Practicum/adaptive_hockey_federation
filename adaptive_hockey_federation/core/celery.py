import os

from celery import Celery

# Запуск
# Поднимается контейнер с Redis infra/docker-compose.redis_cli.yaml
# из директории с manage.py выполнить
# poetry run celery -A <имя экземпляра Celery> worker -Q <перечислить очереди через запятую> -P solo - запуск менеджера задач  # noqa: E501
# Для unix систем можно выполнить флаг -D что бы запустить в фоновом режиме
# из директории с manage.py выполнить
# poetry run celery -A <имя экземпляра Celery> flower - подключить веб интерфес с задачами. По умолчанию localhost:5555 # noqa: E501

# https://docs.celeryq.dev/en/stable/userguide/routing.html
# from kombu import Queue


# get config from https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html # noqa: E501

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.dev_settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

# считываеь все tasks в приложениях
app.autodiscover_tasks()

# в очередь поступают задачи по 1
# app.conf.worker_prefetch_multiplier = 1

# используется приоритет родителей, если такие присутствуют
# app.conf.task_inherit_parent_priority = True

# очередь которая будет использоваться,
# если явно не передана в аргументы apply_async()
# можно не указывать если не планируется использовать несколько очередей.
# по умолчанию будет 'default'
app.conf.task_default_queue = "default_queue"

# Приоритет для брокера

# cортирует по имени очереди ord(),
# а - будет самая приоритетная. Работает не стабильно
# app.conf.broker_transport_options = {"queue_order_strategy": "sorted"}

# работает по указанию аргумента
# в сигнатуре вызова apply_async() arg - priority.
# От 0 до 255, где 0 самая приоритетная
# https://docs.celeryq.dev/en/stable/userguide/routing.html#redis-message-priorities
app.conf.broker_transport_options = {
    "queue_order_strategy": "priority",
}

# Можно указать несколько очередей
# app.conf.task_queues = (
#     Queue("a-high"),
#     Queue("b-medium"),
#     Queue("c-low"),
# )

# если нужно связать на постоянной основе tasks с конкретной очередью

# app.conf.task_routes = {
#     'video_api.tasks.test_low_priority_task': {
#         'queue': 'c-low',
#         'routing_key': 'c-low.priority',
#     },
#     'video_api.tasks.test_high_priority_task': {
#         'queue': 'a-high',
#         'routing_key': 'a-high.priority',
#     },
# }
