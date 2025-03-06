import pytest

from config.config import settings
from test.utils.upload_test_data import load_files

pytest_plugins = ("celery.contrib.pytest",)  # <-- Important!

# @pytest.fixture(scope="session")
# def celery_config():
#     return {
#         "broker_url": settings.RABBITMQ_URL,
#         "result_backend": settings.REDIS_URL,
#         "beat_max_loop_interval": 6,
#         "worker_max_tasks_per_child": 2,
#         "task_serializer": 'json',
#         "result_serializer": 'json',
#         "timezone": 'Asia/Novosibirsk',
#         "broker_connection_retry_on_startup": True
#     }
#
# @pytest.fixture
# def celery_worker_parameters():
#     return {
#         'perform_ping_check': False,
#     }
#
#
# @pytest.fixture(scope='session')
# def celery_includes():
#     return [
#         'services.work_with_pages_service.tasks',
#     ]
#
# @pytest.fixture(scope='session')
# def celery_worker_pool():
#     return 'prefork'

@pytest.fixture(scope="session")
def load_html():
    return [load_files(f"page_{ind}", "html") for ind in range(2)]

@pytest.fixture(scope="session")
def load_xml():
    return [load_files(f"xml_file_{ind}", "xml") for ind in range(20)]
