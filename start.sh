#!/bin/bash
# Script para levantar el backend local con variables de entorno

set -a
source .env.example
source .env 2>/dev/null || true
set +a

echo "=========================================="
echo "  Logistics Route Management API"
echo "=========================================="
echo ""
echo "Variables de entorno cargadas:"
echo "  DB_HOST: $DB_HOST"
echo "  DB_NAME: $DB_NAME"
echo "  DB_USER: $DB_USER"
echo "  DEBUG: $DEBUG"
echo ""

# Crear directorio de logs si no existe
mkdir -p logs

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --noinput

# Crear usuario admin por defecto si no existe
echo "Creando usuario admin por defecto..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
	User.objects.create_superuser('admin', 'admin@local', 'admin123')
END

# Crear token para usuario admin
echo "Creando token para usuario admin..."
python manage.py drf_create_token admin || true

echo ""
echo "=========================================="
echo "  ✅ Servidor corriendo en:"
echo "     http://localhost:8080"
echo "=========================================="
echo ""

# Iniciar servidor
python manage.py runserver 0.0.0.0:8080
