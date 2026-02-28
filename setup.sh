#!/bin/bash

# Setup Script para Logistics Route Management API
# Uso: bash setup.sh

echo "🚀 Iniciando setup de Logistics Route Management API..."

# Crear virtual environment
echo "📦 Creando virtual environment..."
python -m venv venv

# Activar virtual environment
echo "✅ Activando virtual environment..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorio de logs
mkdir -p logs

# Crear directorio de media
mkdir -p media

# Crear directorio de staticfiles
mkdir -p staticfiles

# Ejecutar migraciones
echo "🗄️  Aplicando migraciones..."
python manage.py migrate --noinput

# Crear superusuario (opcional)
echo ""
echo "👤 Crear superusuario (opcional)?"
echo "Ingrese datos para crear administrador:"
python manage.py createsuperuser

# Recolectar estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "✨ ¡Setup completado exitosamente!"
echo ""
echo "🎯 Próximos pasos:"
echo "1. Activar virtual environment: source venv/bin/activate"
echo "2. Iniciar servidor: python manage.py runserver 0.0.0.0:8000"
echo "3. Acceder a: http://localhost:8000/api/"
echo "4. Admin: http://localhost:8000/admin/"
echo ""
