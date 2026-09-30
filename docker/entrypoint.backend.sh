#!/bin/sh
set -e

echo "Running database migrations (alembic upgrade head)..."
alembic -c backend/alembic.ini upgrade head

echo "Starting uvicorn..."
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
