#!/bin/sh
set -e

echo "--------------------------------------------"
echo "[Entrypoint] Starting Logistics API"
echo "--------------------------------------------"

DB_HOST=${DB_HOST:-172.17.0.1}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-logistics}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}

MAX_ATTEMPTS=30
SLEEP_SECONDS=2

echo "[Entrypoint] Waiting for PostgreSQL at $DB_HOST:$DB_PORT (db=$DB_NAME user=$DB_USER)"

attempt=1
while [ $attempt -le $MAX_ATTEMPTS ]; do
  echo "[Entrypoint] Attempt $attempt/$MAX_ATTEMPTS ..."
  if PGPASSWORD="$DB_PASSWORD" psql \
      -h "$DB_HOST" \
      -U "$DB_USER" \
      -p "$DB_PORT" \
      -d "$DB_NAME" \
      -c '\q' \
      --connect-timeout=2 >/dev/null 2>&1; then
    echo "[Entrypoint] PostgreSQL ready"
    break
  fi

  if [ $attempt -eq $MAX_ATTEMPTS ]; then
    echo "[Entrypoint] ERROR: Could not connect to PostgreSQL after $MAX_ATTEMPTS attempts"
    exit 1
  fi

  attempt=$((attempt+1))
  sleep $SLEEP_SECONDS
done

echo "[Entrypoint] Running initial SQL if needed..."

if [ -f "/app/db/init.sql" ]; then
  PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    -p "$DB_PORT" \
    -d "$DB_NAME" \
    -f /app/db/init.sql || true
fi

echo "[Entrypoint] Running Django migrations..."
python manage.py migrate --noinput

echo "[Entrypoint] Creating admin user if not exists..."

python manage.py shell << 'END'
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@local", "admin123")
    print("Admin user created")
else:
    print("Admin user already exists")
END

echo "[Entrypoint] Creating token..."
python manage.py drf_create_token admin || true

echo "[Entrypoint] Collecting static files..."
python manage.py collectstatic --noinput || true

echo "[Entrypoint] Starting Gunicorn..."

exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8080 \
  --workers 2 \
  --worker-class gthread \
  --threads 4 \
  --timeout 120 \
  --graceful-timeout 60 \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  --keep-alive 5 \
  --access-logfile - \
  --error-logfile -
