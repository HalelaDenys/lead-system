#!/usr/bin/env sh
set -e

echo "Waiting for Postgres..."
until pg_isready -h "${APP_CONFIG__DB__HOST}" -U "${APP_CONFIG__DB__USER}" -d "${APP_CONFIG__DB__DB}"; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is ready! Running migrations..."
uv run python -m alembic -c src/alembic.ini upgrade head

echo "Starting API..."
exec uv run python src/landing_service/main.py
