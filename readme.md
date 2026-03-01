# Logistics Route Management API

**API profesional para gestión integral de rutas logísticas**

Sistema de gestión y optimización de rutas con Django REST Framework 3.14 y PostgreSQL 16.

**Características principales:**
- Importación masiva desde Excel (5000+ registros en ~5 segundos)
- CRUD completo de rutas con validación automática
- Ejecución individual y por lotes
- Auditoría completa de todas las operaciones
- 25 endpoints REST totalmente documentados
- Autenticación Token-based
- Documentación interactiva (Swagger + ReDoc + OpenAPI 3.0)

## Estándar de Respuestas

Todas las rutas de API siguen un estándar consistente de respuestas definido en [`apps/routes/utils/response.py`](apps/routes/utils/response.py):

### Respuesta Exitosa

```json
{
  "success": true,
  "message": "Listado de rutas",
  "data": [...],
  "meta": {
    "timestamp": "2026-03-01T10:30:00.000Z",
    "version": "v1"
  }
}
```

### Respuesta con Error

```json
{
  "success": false,
  "error": {
    "message": "No file provided",
    "code": "NO_FILE_ERROR",
    "meta": {
      "timestamp": "2026-03-01T10:30:00.000Z",
      "version": "v1"
    }
  }
}
```

### Con Paginación

```json
{
  "success": true,
  "message": "Listado de rutas",
  "data": [...],
  "meta": {
    "timestamp": "2026-03-01T10:30:00.000Z",
    "pagination": {
      "current_page": 1,
      "per_page": 25,
      "total_items": 150,
      "total_pages": 6
    }
  }
}
```

## �📋 Requisitos Previos

- Python 3.10+
- PostgreSQL 16 (vía Docker)
- Docker & Docker Compose
- pip

## Quick Start

### Opción 1: TODO en UN COMANDO (Docker Compose)

**Base de datos + Backend automáticamente:**

```bash
docker compose up
```

Eso es. El comando automáticamente:
- Levanta PostgreSQL 16
- Ejecuta migraciones de Django
- Levanta el servidor Django en http://localhost:8080

**Ver logs:**

```bash
docker compose logs -f
```

**Detener todo:**

```bash
docker compose down
```

---

### Opción 2: Backend Local + BD en Docker

Si prefieres desarrollo local sin Docker para el backend:

#### Paso 1: Levantar solo PostgreSQL

```bash
docker compose up -d postgres
```

#### Paso 2: Instalar dependencias locales (solo una vez)

```bash
pip install -r requirements.txt
```

#### Paso 3: Ejecutar migraciones

```bash
python manage.py migrate
```

#### Paso 4: Iniciar el servidor local

```bash
python manage.py runserver 0.0.0.0:8000
```

#### Variables de Entorno (desarrollo local)

```bash
DB_PORT=5432
DB_NAME=logistics
DB_USER=postgres
DB_PASSWORD=postgres
DEBUG=True
```

---

### Comparación: Docker vs Local

| Aspecto | Docker Compose | Backend Local |
|--------|---|---|
| **Comando** | `docker compose up` | `python manage.py runserver` |
| **Setup** | Automático | Manual (pip install) |
| **Aislamiento** | Contenedorizado | Directo en máquina |
| **Desarrollo** | Lento | Rápido (hot reload) |
| **Producción** | ✅ Recomendado | ❌ No recomendado |

## Endpoints Principales

La API incluye **25 endpoints REST** organizados en las siguientes categorías:

**Autenticación (1):**
- `POST /api/token-auth/` - Obtener token de autenticación

**Rutas (11):**
```
GET    /api/routes/                  - Listar todas las rutas (paginado)
POST   /api/routes/                  - Crear nueva ruta
GET    /api/routes/{id}/             - Obtener detalle de ruta
PUT    /api/routes/{id}/             - Actualizar ruta
PATCH  /api/routes/{id}/             - Actualización parcial
DELETE /api/routes/{id}/             - Eliminar ruta
POST   /api/routes/import/           - Importar masivamente desde Excel
POST   /api/routes/{id}/execute/     - Ejecutar ruta individual
POST   /api/routes/execute_routes/   - Ejecutar múltiples rutas
GET    /api/routes/statistics/       - Estadísticas globales del sistema
GET    /api/routes/execution_history/- Historial de ejecuciones de una ruta
```

**Catálogos (6):**
```
GET    /api/route-statuses/          - Listar estados disponibles
GET    /api/route-statuses/{id}/     - Detalle de un estado
GET    /api/locations/               - Listar/buscar ubicaciones
GET    /api/locations/{id}/          - Detalle de una ubicación
```

**Registros (4):**
```
GET    /api/execution-logs/          - Historial de ejecuciones
GET    /api/execution-logs/{id}/     - Detalle de una ejecución
GET    /api/import-batches/          - Historial de importaciones
GET    /api/import-batches/{id}/     - Detalle de un lote importado
```

Ver documentación completa en Swagger UI: http://localhost:8080/api/docs/

## Documentación de API

Una vez ejecutando el servidor, accede a:

| Servicio | URL | Descripción |
|----------|-----|------------|
| Home | http://localhost:8080/ | Dashboard de inicio |
| Swagger UI | http://localhost:8080/api/docs/ | Documentación interactiva |
| ReDoc | http://localhost:8080/api/redoc/ | Documentación estática |
| OpenAPI Schema | http://localhost:8080/api/schema/ | Especificación OpenAPI 3.0 |
| Admin Panel | http://localhost:8080/admin/ | Panel administrativo Django |

## Estructura del Proyecto

```
.
├── apps/
│   └── routes/
│       ├── domain/          # Modelos ORM (MVT Model)
│       ├── application/     # Lógica de negocio (DDD)
│       ├── infrastructure/  # Acceso a datos
│       └── api/             # Serializers y Views (MVT View/Template)
├── config/
│   ├── settings.py         # Configuración Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # WSGI
├── db/
│   └── init.sql            # Script SQL inicial
├── docker-compose.yml      # Configuración Docker
├── Dockerfile              # Imagen Docker
├── manage.py               # CLI Django
├── requirements.txt        # Dependencias Python
└── readme.md              # Este archivo
```

## Arquitectura

El proyecto implementa dos patrones de arquitectura complementarios:

### MVT (Model-View-Template)

- **Model** (`apps/routes/domain/models.py`): Django ORM models
- **View** (`apps/routes/api/views.py`): REST views (ViewSets)
- **Template** (`apps/routes/api/serializers.py`): JSON serialization (DRF)

### DDD (Domain-Driven Design)

- **Domain Layer**: Modelos, entidades de negocio
- **Application Layer**: Servicios, casos de uso
- **Infrastructure Layer**: Repositorios, acceso a datos
- **API Layer**: Controllers REST, serializers

## Configuración de la Base de Datos

**Tablas principales** (esquema `public`):
- `routes_location` - Ubicaciones geográficas (origen/destino)
- `routes_status` - Catálogo de estados de ruta (7 estados preinsertados)
- `routes_route` - Rutas principales con origen, destino, distancia, prioridad
- `routes_payload` - Payloads JSON asociados a rutas
- `routes_execution_log` - Registro de ejecuciones y resultados
- `routes_import_batch` - Historial de importaciones masivas
- `auth_user` - Usuarios del sistema
- `authtoken_token` - Tokens de autenticación

### Constraints Principales

```sql
-- Ubicaciones: validación de coordenadas
CHECK (latitude BETWEEN -90 AND 90)
CHECK (longitude BETWEEN -180 AND 180)

-- Rutas: distancia positiva
CHECK (distance_km > 0)

-- Foreign Keys con ON DELETE CASCADE
FOREIGN KEY (origin_id) REFERENCES routes_location(id)
FOREIGN KEY (destination_id) REFERENCES routes_location(id)
FOREIGN KEY (status_id) REFERENCES routes_status(id)
FOREIGN KEY (batch_id) REFERENCES routes_import_batch(id)
```

## Docker Compose

### Levantar servicios completos

```bash
docker compose up --build
```

### Levantar solo PostgreSQL (desarrollo local)

```bash
docker compose up -d postgres
```

Espera a que PostgreSQL esté listo. Puedes verificar con:

```bash
docker compose logs postgres
```

### Detener servicios

```bash
docker compose down
```

### Ver Logs

```bash
docker compose logs -f postgres
```

## Dependencias Principales

- **Django 5.0.1** - Framework web
- **djangorestframework 3.14.0** - API REST
- **psycopg2-binary 2.9.10** - Driver PostgreSQL
- **pandas 2.2.3** - Procesamiento de datos
- **drf-spectacular 0.27.0** - Documentación automática de API
- **gunicorn 21.2.0** - Servidor WSGI producción

Ver `requirements.txt` para lista completa.

## Monitoreo y Debugging

### Ver Estado de Servicios Docker

```bash
docker compose ps
```

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker compose logs -f

# Solo PostgreSQL
docker compose logs -f postgres

# Solo Django
docker compose logs -f django
```

### Conectar a PostgreSQL

```bash
psql -h localhost -U postgres -d logistics
```

### Ver Migraciones de Django

```bash
python manage.py showmigrations
```

### Logs de la Aplicación

Los logs se guardan automáticamente en el directorio `logs/`:

```
logs/
├── django.log      # Logs generales de Django
├── error.log       # Errores capturados
└── api.log         # Logs detallados de la API
```

**Ver logs en tiempo real (backend local):**

```bash
tail -f logs/django.log
tail -f logs/error.log
tail -f logs/api.log
```

### Crear Superusuario

```bash
python manage.py createsuperuser
```

## Despliegue en Producción

```bash
docker compose -f docker-compose.prod.yml up -d
```

**Requisitos antes de producción**:

1. Cambiar SECRET_KEY en .env
2. Cambiar contraseña de PostgreSQL
3. Configurar DEBUG=False
4. Configurar ALLOWED_HOSTS correctamente
5. Guardar credenciales en variables de entorno seguras
6. Configurar SSL/HTTPS

## Desarrollado por

Jose Trespalacios B.

## Licencia

Privada - Falabella

## Soporte

Para reportar issues o sugerencias, contacta al equipo de desarrollo.

---

**Última actualización**: Marzo 2026
**Versión**: 1.0.0 Producción (Listo para deployment)
