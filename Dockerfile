FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.1.1

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} gunicorn

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app/
