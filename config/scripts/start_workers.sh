#!/bin/bash
celery -A services.my_celery worker --loglevel=info