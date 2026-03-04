#!/bin/bash

# Script para corregir CORS en producción
# Ejecutar en el servidor: bash fix-cors.sh

set -e

echo "🔧 CORRIGIENDO CONFIGURACIÓN DE CORS..."
echo ""

# ========== PASO 1: Actualizar Backend ==========
echo "📦 1. Actualizando Backend..."
cd /var/www/logistics/api

# Descargar cambios
git pull origin main

# Reiniciar Docker
docker-compose down
docker-compose up -d --build

echo "✅ Backend reiniciado"
echo ""

# ========== PASO 2: Actualizar Nginx ==========
echo "🔄 2. Actualizando configuración de Nginx..."

# Crear backup
sudo cp /etc/nginx/sites-available/logistics /etc/nginx/sites-available/logistics.backup

# Crear archivo temporal con la configuración correcta
sudo tee /etc/nginx/sites-available/logistics > /dev/null << 'EOF'
########################################################
# FRONTEND - logistics.josetrespalaciosbedoya.co
########################################################

server {
    listen 80;
    server_name logistics.josetrespalaciosbedoya.co;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name logistics.josetrespalaciosbedoya.co;

    ssl_certificate /etc/letsencrypt/live/logistics.josetrespalaciosbedoya.co/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/logistics.josetrespalaciosbedoya.co/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    root /var/www/logistics/web/dist/logistics-frontend/browser;
    index index.csr.html;

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        try_files $uri $uri/ /index.csr.html;
    }
}

########################################################
# BACKEND - api.logistics.josetrespalaciosbedoya.co
########################################################

server {
    listen 80;
    server_name api.logistics.josetrespalaciosbedoya.co;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.logistics.josetrespalaciosbedoya.co;

    ssl_certificate /etc/letsencrypt/live/logistics.josetrespalaciosbedoya.co/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/logistics.josetrespalaciosbedoya.co/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Map origen permitido
    map $http_origin $cors_origin {
        default "";
        "~^https?://logistics\.josetrespalaciosbedoya\.co$" $http_origin;
        "~^https?://api\.logistics\.josetrespalaciosbedoya\.co$" $http_origin;
    }

    location / {
        # Manejo de solicitudes OPTIONS (preflight CORS)
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' $cors_origin always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, PATCH, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Accept, Authorization, Cache-Control, Content-Type, DNT, If-Modified-Since, Keep-Alive, Origin, User-Agent, X-Requested-With, X-CSRFToken' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Access-Control-Max-Age' '86400' always;
            add_header 'Content-Length' '0' always;
            add_header 'Content-Type' 'text/plain charset=UTF-8' always;
            return 204;
        }

        proxy_pass http://127.0.0.1:8080;

        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_redirect off;

        # CORS headers para respuestas exitosas
        add_header 'Access-Control-Allow-Origin' $cors_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, PATCH, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Accept, Authorization, Cache-Control, Content-Type, DNT, If-Modified-Since, Keep-Alive, Origin, User-Agent, X-Requested-With, X-CSRFToken' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
    }
}
EOF

echo "✅ Nginx configurado"
echo ""

# Verificar sintaxis
echo "🔍 Verificando sintaxis de Nginx..."
sudo nginx -t
echo "✅ Sintaxis correcta"
echo ""

# ========== PASO 3: Recargar Nginx ==========
echo "🔄 3. Recargando Nginx..."
sudo systemctl reload nginx
sudo systemctl restart nginx
echo "✅ Nginx reiniciado"
echo ""

# ========== PASO 4: Recompilar Frontend ==========
echo "🎨 4. Compilando Frontend..."
cd /var/www/logistics/web
git pull origin main
npm install
npm run build
echo "✅ Frontend compilado"
echo ""

# ========== VERIFICACIÓN ==========
echo "════════════════════════════════════"
echo "✅ CORS CORREGIDO EXITOSAMENTE"
echo "════════════════════════════════════"
echo ""
echo "📋 Estado de servicios:"
cd /var/www/logistics/api
docker-compose ps
echo ""
echo "🌐 URLs:"
echo "  Frontend: https://logistics.josetrespalaciosbedoya.co"
echo "  API: https://api.logistics.josetrespalaciosbedoya.co/api"
echo ""
echo "✅ SISTEMA LISTO"
