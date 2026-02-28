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

echo ""
echo "=========================================="
echo "  ✅ Servidor corriendo en:"
echo "     http://localhost:8080"
echo "=========================================="
echo ""

# Iniciar servidor
python manage.py runserver 0.0.0.0:8080
