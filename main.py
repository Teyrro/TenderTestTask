import redis
from celery import Celery

from config import settings

mul_celery = Celery(
    "mul_celery",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
)
mul_celery.conf.broker_connection_retry_on_startup = True

@mul_celery.task
def mul(x, y):
    return x * y

