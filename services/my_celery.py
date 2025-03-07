from __future__ import absolute_import, unicode_literals
from celery import Celery

from config.config import settings

app = Celery(
    "tasks",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,

)


app.conf.update(
    beat_max_loop_interval=6,
    worker_max_tasks_per_child=4,
    task_serializer='json',
    result_serializer='json',
    timezone = 'Asia/Novosibirsk',
    broker_connection_retry_on_startup = True
)
app.autodiscover_tasks(["services.work_with_pages_service"])

