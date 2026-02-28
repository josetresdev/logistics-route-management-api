@echo off
REM Script para levantar el backend local con variables de entorno en Windows

echo ==========================================
echo   Logistics Route Management API
echo ==========================================
echo.
echo Cargando variables de entorno desde .env
echo.

REM Cargar variables de entorno desde .env.example
for /f "usebackq delims==" %%i in (.env.example) do (
    if not "%%i"=="" (
        for /f "usebackq tokens=1* delims==" %%a in ("%%i") do (
            set "%%a=%%b"
        )
    )
)

REM Sobreescribir con .env si existe
if exist .env (
    for /f "usebackq delims==" %%i in (.env) do (
        if not "%%i"=="" (
            for /f "usebackq tokens=1* delims==" %%a in ("%%i") do (
                set "%%a=%%b"
            )
        )
    )
)

echo Variables de entorno:
echo   DB_HOST: %DB_HOST%
echo   DB_NAME: %DB_NAME%
echo   DB_USER: %DB_USER%
echo   DEBUG: %DEBUG%
echo.

REM Crear directorio de logs si no existe
if not exist logs mkdir logs

REM Ejecutar migraciones
echo Ejecutando migraciones...
python manage.py migrate --noinput

echo.
echo ==========================================
echo   ^= Servidor corriendo en:
echo      http://localhost:8080
echo ==========================================
echo.

REM Iniciar servidor
python manage.py runserver 0.0.0.0:8080

pause
