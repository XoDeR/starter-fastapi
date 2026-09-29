#!/bin/sh
set -eu

attempts=15
i=1
until uv run alembic upgrade head; do
  if [ "$i" -ge "$attempts" ]; then
    echo "database migrations failed after ${attempts} attempts" >&2
    exit 1
  fi
  echo "database not ready, retrying (${i}/${attempts})..."
  i=$((i + 1))
  sleep 2
done

exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${API_PORT:-8000}" --reload
