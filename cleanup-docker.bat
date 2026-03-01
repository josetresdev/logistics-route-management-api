@echo off
REM =========================================================
REM SCRIPT DE LIMPIEZA COMPLETA DE DOCKER
REM =========================================================
REM Este script:
REM 1. Detiene todos los contenedores
REM 2. Elimina los contenedores
REM 3. Elimina volúmenes (incluyendo base de datos)
REM 4. Elimina redes
REM =========================================================

echo.
echo [*] Deteniendo contenedores...
docker-compose down

echo.
echo [*] Removiendo volúmenes (datos persistentes)...
docker-compose down -v

echo.
echo [*] Limpiando contenedores no usados...
docker container prune -f

echo.
echo [*] Limpiando volúmenes no usados...
docker volume prune -f

echo.
echo [*] Limpiando redes no usadas...
docker network prune -f

echo.
echo [✓] LIMPIEZA COMPLETADA
echo.
echo Para iniciar de nuevo:
echo   docker-compose up -d
echo.
pause
