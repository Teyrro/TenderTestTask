FROM python:3.11-slim AS builder

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

ADD poetry.lock pyproject.toml poetry.toml ./
RUN pip install poetry
RUN poetry env use 3.11
RUN poetry install --no-root --no-interaction --no-ansi


FROM python:3.11-slim AS final

WORKDIR /code
COPY --from=builder .venv/ /.venv
ENV PATH="/.venv/bin:$PATH" \
    REDIS_MASTER_HOST=$REDIS_MASTER_HOST \
    RABBITMQ_HOST=$RABBITMQ_HOST

COPY .env ./
COPY config /code/config
COPY services /code/services
COPY test /code/test

RUN chmod 777 config/scripts/worker.sh

