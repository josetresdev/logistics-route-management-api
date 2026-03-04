#!/bin/sh
set -e

echo "--------------------------------------------"
echo "[Entrypoint] Starting Logistics API"
echo "--------------------------------------------"

DB_HOST=${DB_HOST:-host.docker.internal}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-logistics}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}

echo "[Entrypoint] Waiting for PostgreSQL at $DB_HOST:$DB_PORT"

for i in $(seq 1 30); do
  if PGPASSWORD=$DB_PASSWORD psql \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    -p "$DB_PORT" \
    -d "$DB_NAME" \
    -c '\q' \
    --connect-timeout=2 >/dev/null 2>&1; then
    echo "[Entrypoint] PostgreSQL ready"
    break
  fi

  echo "[Entrypoint] Attempt $i/30..."
  sleep 2
done

echo "[Entrypoint] Running migrations"
python manage.py migrate --noinput

echo "[Entrypoint] Collecting static"
python manage.py collectstatic --noinput || true

echo "[Entrypoint] Starting Gunicorn"

exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8080 \
  --workers 2 \
  --worker-class gthread \
  --threads 4 \
  --timeout 120
