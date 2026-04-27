FROM python:3.11-slim

ENV PYTHONPATH=src

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y gcc curl \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN pip install --no-cache-dir uv \
    && uv sync

COPY .env.exapmle /app/.env.exapmle
COPY src/alembic.ini /app/src/alembic.ini
COPY src/alembic /app/src/alembic
COPY src/infrastructure /app/src/infrastructure
COPY src/shared /app/src/shared
COPY src/core_service /app/src/core_service
COPY src/seed_db.py /app/src/seed_db.py
COPY entrypoint_core.sh /app/entrypoint_core.sh

RUN chmod +x /app/entrypoint_core.sh
