#!/bin/sh
set -e

echo "[Entrypoint] Ejecutando migraciones..."
while ! python manage.py migrate --noinput; do
  echo "[Entrypoint] Esperando a la base de datos para migrar..."
  sleep 3
done

echo "[Entrypoint] Intentando crear usuario admin..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user_exists = User.objects.filter(username='admin').exists(); print('Usuario admin ya existe' if user_exists else User.objects.create_superuser('admin', 'admin@local', 'admin123'))"
rc=$?
if [ $rc -ne 0 ]; then
  echo "[Entrypoint] ERROR: Falló la creación del usuario admin."
  exit $rc
fi

echo "[Entrypoint] Intentando crear token para admin..."
python manage.py drf_create_token admin || true

echo "[Entrypoint] Arrancando Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 4 --access-logfile logs/access.log --error-logfile logs/error.log
