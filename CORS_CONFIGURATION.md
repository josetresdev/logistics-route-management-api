# 🔧 CONFIGURACIÓN DE CORS - RESUMEN DE CORRECCIONES

## ✅ Problemas Identificados y Solucionados

### 🔴 Error Original
```
Solicitud desde otro origen bloqueada: la política de mismo origen impide leer el recurso remoto
en https://api.logistics.josetrespalaciosbedoya.co/api//token-auth/
(razón: falta la cabecera CORS 'Access-Control-Allow-Origin')
```

---

## 📝 CORRECCIONES REALIZADAS

### 1. **Frontend - Configuración de URLs**

#### Archivos Modificados:
- `src/environments/environment.ts`
- `src/environments/environment.prod.ts`

#### Cambio:
```typescript
// ❌ ANTES (URL con trailing slash)
apiUrl: 'https://api.logistics.josetrespalaciosbedoya.co/api/'

// ✅ DESPUÉS (Sin trailing slash)
apiUrl: 'https://api.logistics.josetrespalaciosbedoya.co/api'
```

**Razón:** El trailing slash causaba doble slash `//token-auth/` que es inválido.

---

### 2. **Frontend - Interceptor HTTP CORS**

#### Archivo Modificado:
- `src/app/core/interceptors/api.interceptor.ts`

#### Cambio:
```typescript
// ❌ ANTES (Sin withCredentials)
request = request.clone({
  setHeaders: headers
});

// ✅ DESPUÉS (Con withCredentials para CORS)
request = request.clone({
  setHeaders: headers,
  withCredentials: true
});
```

**Razón:** `withCredentials: true` es esencial para solicitudes CORS con credenciales.

---

### 3. **Backend - Configuración CORS en Django**

#### Archivo Modificado:
- `config/settings.py`

#### Cambios Agregados:
```python
# CORS Configuration completa
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

CORS_ALLOW_CREDENTIALS = True

# Headers explícitos
CORS_ALLOW_HEADERS = [
    "accept", "accept-encoding", "authorization", "content-type",
    "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT",
]

CORS_EXPOSE_HEADERS = [
    "content-type", "x-csrftoken",
]

CORS_MAX_AGE = 86400  # 24 horas para preflight cache

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
```

---

### 4. **Backend - Variables de Entorno (.env)**

#### Archivo Modificado:
- `.env`

#### Configuración CORS:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:4200,http://127.0.0.1:4200,http://localhost:8000,http://127.0.0.1:8000,http://localhost:80,http://127.0.0.1:80,https://api.logistics.josetrespalaciosbedoya.co,https://logistics.josetrespalaciosbedoya.co

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,api.logistics.josetrespalaciosbedoya.co,logistics.josetrespalaciosbedoya.co
```

---

### 5. **Nginx - Configuración CORS en Reverse Proxy**

#### Archivo Modificado:
- `nginx.conf`

#### Cambios:
```nginx
# Mapa para validar orígenes permitidos
map $http_origin $cors_origin {
    default "";
    ~^https?://(localhost|127\.0\.0\.1)(:(3000|4200|8000|8080))?$ $http_origin;
    ~^https?://api\.logistics\.josetrespalaciosbedoya\.co$ $http_origin;
    ~^https?://logistics\.josetrespalaciosbedoya\.co$ $http_origin;
}

# Manejo de solicitudes OPTIONS (preflight)
if ($request_method = 'OPTIONS') {
    add_header 'Access-Control-Allow-Origin' $cors_origin always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, PATCH, OPTIONS' always;
    add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,X-CSRFToken' always;
    add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range,Content-Type' always;
    add_header 'Access-Control-Allow-Credentials' 'true' always;
    add_header 'Access-Control-Max-Age' '86400' always;
    return 204;
}

# Headers CORS en todas las respuestas
add_header 'Access-Control-Allow-Origin' $cors_origin always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, PATCH, OPTIONS' always;
add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,X-CSRFToken' always;
```

---

### 6. **Docker Compose Producción**

#### Archivo Modificado:
- `docker-compose.prod.yml`

#### Cambio:
```yaml
# ✅ Agregado: Pasar CORS_ALLOWED_ORIGINS al contenedor
environment:
  ...
  CORS_ALLOWED_ORIGINS: ${CORS_ALLOWED_ORIGINS}
  ...
```

---

## 🧪 VALIDACIÓN

### Crear archivo de prueba
```bash
python validate_cors.py
```

### Resultado Esperado:
```
✓ CORS preflight exitoso
✓ CORS preflight exitoso
...
✓ Todas las configuraciones de CORS están correctas
```

---

## 🚀 PASOS PARA DESPLEGAR

### Desarrollo (Local)
```bash
# 1. Actualizar variables de entorno
# Ya configurado en .env

# 2. Reiniciar Django
python manage.py runserver 8000

# 3. En otra terminal, verificar CORS
python validate_cors.py
```

### Producción (Docker)
```bash
# 1. Rebuild con nueva configuración
docker-compose -f docker-compose.prod.yml build

# 2. Iniciar servicios
docker-compose -f docker-compose.prod.yml up -d

# 3. Verificar logs
docker-compose -f docker-compose.prod.yml logs -f web
```

---

## 🔍 ORÍGENES PERMITIDOS

### Desarrollo
- ✅ `http://localhost:3000` (React/Angular default)
- ✅ `http://localhost:4200` (Angular default)
- ✅ `http://localhost:8000` (Django default)
- ✅ `http://127.0.0.1:*` (Localhost local)

### Producción
- ✅ `https://api.logistics.josetrespalaciosbedoya.co` (API)
- ✅ `https://logistics.josetrespalaciosbedoya.co` (Frontend)

---

## ⚕️ HEADERS CORS EXPLICADOS

| Header | Propósito |
|--------|-----------|
| `Access-Control-Allow-Origin` | Especifica qué orígenes pueden acceder |
| `Access-Control-Allow-Methods` | Métodos HTTP permitidos (GET, POST, etc) |
| `Access-Control-Allow-Headers` | Headers que el cliente puede enviar |
| `Access-Control-Max-Age` | Cuántos segundos cachear preflight (3600s = 1h) |
| `Access-Control-Allow-Credentials` | Permitir cookies/credenciales en requests |

---

## 📋 CHECKLIST DE VALIDACIÓN

- [x] URLs sin trailing slash
- [x] `withCredentials: true` en interceptor Angular
- [x] CORS configurado en `settings.py`
- [x] Variables CORS en `.env`
- [x] Nginx con soporte CORS completo
- [x] Docker Compose con variables CORS
- [x] Script de validación disponible
- [x] Orígenes permitidos configurados

---

## 🐛 TROUBLESHOOTING

### Si aún ves error de CORS:

1. **Verificar que DEBUG=False en producción** (nginx solo leerá CORS_ALLOWED_ORIGINS)
   ```bash
   echo $DEBUG  # Debe ser False o vacio
   ```

2. **Reiniciar Docker**
   ```bash
   docker-compose restart web nginx
   ```

3. **Limpiar browser cache**
   - F12 → Network → Disable cache
   - O abrir en incognito

4. **Verificar logs**
   ```bash
   docker-compose logs -f web
   docker-compose logs -f nginx
   ```

5. **Probar endpoint CORS manualmente**
   ```bash
   curl -H "Origin: https://api.logistics.josetrespalaciosbedoya.co" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        https://api.logistics.josetrespalaciosbedoya.co/api/token-auth/ \
        -v
   ```

---

## 📚 RECURSOS

- [MDN - CORS](https://developer.mozilla.org/es/docs/Web/HTTP/CORS)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)
- [Angular HttpClient CORS](https://angular.io/guide/http-security)
- [Nginx CORS Configuration](https://enable-cors.org/server_nginx.html)

---

**Versión:** 1.0
**Fecha:** 2026-03-04
**Estado:** ✅ COMPLETO
