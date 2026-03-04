#!/bin/sh
set -e

echo "--------------------------------------------"
echo "[Entrypoint] Starting Logistics API"
echo "--------------------------------------------"

DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-logistics}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}

echo "[Entrypoint] Waiting for PostgreSQL..."

# Esperar conexión real con password
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' >/dev/null 2>&1
do
  echo "[Entrypoint] PostgreSQL not ready yet..."
  sleep 3
done

echo "[Entrypoint] PostgreSQL ready"

echo "[Entrypoint] Running migrations..."
python manage.py migrate --noinput

echo "[Entrypoint] Creating admin user if not exists..."

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        "admin",
        "admin@local",
        "admin123"
    )
    print("Admin user created")
else:
    print("Admin user already exists")
END

echo "[Entrypoint] Creating token (if not exists)..."
python manage.py drf_create_token admin || true

echo "[Entrypoint] Collecting static files..."
python manage.py collectstatic --noinput || true

echo "[Entrypoint] Starting Gunicorn..."

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 3 \
    --worker-class gthread \
    --threads 4 \
    --timeout 120 \
    --graceful-timeout 60 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile -
