@echo off
REM Setup Script para Logistics Route Management API - Windows
REM Uso: setup.bat

echo.
echo 🚀 Iniciando setup de Logistics Route Management API...
echo.

REM Crear virtual environment
echo 📦 Creando virtual environment...
python -m venv venv

REM Activar virtual environment
echo ✅ Activando virtual environment...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📚 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Crear directorios
mkdir logs 2>nul
mkdir media 2>nul
mkdir staticfiles 2>nul

REM Ejecutar migraciones
echo 🗄️  Aplicando migraciones...
python manage.py migrate --noinput

REM Crear superusuario
echo.
echo 👤 Crear superusuario?
echo Presione Enter para continuar...
pause
python manage.py createsuperuser

REM Recolectar estáticos
echo 📁 Recolectando archivos estáticos...
python manage.py collectstatic --noinput

echo.
echo ✨ ¡Setup completado exitosamente!
echo.
echo 🎯 Próximos pasos:
echo 1. Activar virtual environment: venv\Scripts\activate.bat
echo 2. Iniciar servidor: python manage.py runserver 0.0.0.0:8000
echo 3. Acceder a: http://localhost:8000/api/
echo 4. Admin: http://localhost:8000/admin/
echo.
pause
