FROM python:3.11

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1



RUN curl -sSL https://install.python-poetry.org | python3

WORKDIR /code

ADD poetry.lock pyproject.toml poetry.toml .env /code/

ENV REDIS_MASTER_HOST=$REDIS_MASTER_HOST
ENV RABBITMQ_HOST=$RABBITMQ_HOST

RUN poetry install --no-root --no-interaction --no-ansi

ADD config /code/config
ADD services /code/services
ADD test /code/test

RUN chmod 777 config/scripts/worker.sh

