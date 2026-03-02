#!/bin/sh

echo "[Entrypoint] Waiting for database..."

DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}

while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"
do
  echo "[Entrypoint] Database not ready yet..."
  sleep 3
done

echo "[Entrypoint] Running migrations..."
python manage.py migrate --noinput

echo "[Entrypoint] Creating superuser if not exists..."
python manage.py shell -c "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
exists = User.objects.filter(username='admin').exists(); \
print('Admin exists' if exists else User.objects.create_superuser('admin', 'admin@local', 'admin123'))"

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
