#!/usr/bin/env pwsh
# =========================================================
# SCRIPT DE LIMPIEZA COMPLETA DE DOCKER (PowerShell)
# =========================================================
# Este script:
# 1. Detiene todos los contenedores
# 2. Elimina los contenedores
# 3. Elimina volúmenes (incluyendo base de datos)
# 4. Elimina redes

Write-Host ""
Write-Host "[*] Deteniendo contenedores..." -ForegroundColor Cyan
docker-compose down

Write-Host ""
Write-Host "[*] Removiendo volúmenes (datos persistentes)..." -ForegroundColor Yellow
docker-compose down -v

Write-Host ""
Write-Host "[*] Limpiando contenedores no usados..." -ForegroundColor Cyan
docker container prune -f

Write-Host ""
Write-Host "[*] Limpiando volúmenes no usados..." -ForegroundColor Cyan
docker volume prune -f

Write-Host ""
Write-Host "[*] Limpiando redes no usadas..." -ForegroundColor Cyan
docker network prune -f

Write-Host ""
Write-Host "[✓] LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar de nuevo:" -ForegroundColor Cyan
Write-Host "  docker-compose up -d" -ForegroundColor White
Write-Host ""
