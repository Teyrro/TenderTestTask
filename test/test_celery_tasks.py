from celery.contrib.testing.worker import start_worker

from main import mul_celery, mul


def test_add_task(celery_app, celery_worker):
    @celery_app.task
    def add(x, y):
        return x + y

    celery_worker.reload()
    assert add.delay(4, 4).get(timeout=2) == 8

def test_mul_task_without_fixture():
    with start_worker(  # <-- Important!
        mul_celery, pool="solo", loglevel="info", perform_ping_check=False, shutdown_timeout=30  # <-- Important!
    ) as worker:
        assert mul.delay(4, 4).get(timeout=2) == 16