#!/bin/sh
set -e

echo "[Entrypoint] Waiting for database..."

DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"
do
  echo "[Entrypoint] Database not ready yet..."
  sleep 3
done

echo "[Entrypoint] Database ready"

echo "[Entrypoint] Running migrations..."
python manage.py migrate --noinput

echo "[Entrypoint] Creating admin user if not exists..."

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin","admin@local","admin123")
    print("Admin user created")
else:
    print("Admin user already exists")
END

echo "[Entrypoint] Creating token..."
python manage.py drf_create_token admin || true

echo "[Entrypoint] Collecting static files..."
python manage.py collectstatic --noinput

echo "[Entrypoint] Starting Gunicorn..."

exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8080 \
  --workers 4 \
  --worker-class gthread \
  --threads 2 \
  --timeout 300 \
  --graceful-timeout 60 \
  --access-logfile - \
  --error-logfile -
