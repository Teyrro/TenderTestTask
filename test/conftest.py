import pytest
from config.config import settings
from test.utils.upload_test_data import load_files

pytest_plugins = ("celery.contrib.pytest",)  # <-- Important!


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": settings.RABBITMQ_URL,
        "result_backend": settings.REDIS_URL,
        "beat_max_loop_interval": 3,
        "worker_max_tasks_per_child": 2,
        "task_serializer": 'json',
        "result_serializer": 'json',
        "timezone": 'Asia/Novosibirsk',
        "broker_connection_retry_on_startup": True,
        "task_always_eager": True,  # Отключает синхронное выполнение
        "task_store_eager_result": True,
        "accept_content": ["json"],
        "task_ignore_result": False,
    }


@pytest.fixture
def celery_worker_parameters():
    return {
        'loglevel': 'info',
        'shutdown_timeout': 30,
    }


@pytest.fixture(scope='session')
def celery_includes():
    return [
        'services.work_with_pages_service.tasks',
        "celery.contrib.testing.tasks",
    ]

@pytest.fixture(scope='session')
def celery_worker_pool():
    return 'solo'

@pytest.fixture(scope="session")
def load_html():
    return [load_files(f"page_{ind}", "html") for ind in range(2)]

@pytest.fixture(scope="session")
def load_xml():
    return [load_files(f"xml_file_{ind}", "xml") for ind in range(20)]

