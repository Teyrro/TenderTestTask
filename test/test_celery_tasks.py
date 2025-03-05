from services.my_celery import mul


def test_add_task(celery_app, celery_worker):
    @celery_app.task
    def add(x, y):
        return x + y

    celery_worker.reload()
    assert add.delay(4, 4).get(timeout=2) == 8