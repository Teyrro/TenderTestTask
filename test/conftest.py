import pytest

from config.config import settings

pytest_plugins = ("celery.contrib.pytest",)  # <-- Important!

@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": settings.RABBITMQ_URL,
        "result_backend": settings.REDIS_URL,
    }