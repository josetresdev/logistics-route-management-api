# API de gestión de rutas logísticas

Sistema integral de gestión de rutas logísticas. Aplicación backend construida con Django 5.0 y Django REST Framework. Gestión completa del ciclo de vida: importación, validación, ejecución y auditoría.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red?logo=django)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://www.docker.com/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

---

## Tabla de contenidos

- [Inicio rápido](#inicio-rápido)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Stack técnico](#stack-técnico)
- [Instalación](#instalación)
- [Uso y endpoints](#uso-y-endpoints)
- [Modelos de datos](#modelos-de-datos)
- [Testing](#testing)
- [Docker](#docker)
- [Documentación](#documentación)
- [Contribución](#contribución)

---

## Inicio rápido

### 5 Minutos para ejecutar

#### Windows
```batch
cd logistics-route-management-api
setup.bat
```

#### Linux / macOS
```bash
cd logistics-route-management-api
bash setup.sh
```

#### Docker (Recomendado - Sin Dependencias Locales)
```bash
docker-compose up
```

Acceder a: **http://localhost:8000/api/**

---

## Características

### Funcionalidades Core
- **API REST Completa**: Operaciones CRUD con acciones personalizadas
- **Importación Excel**: Carga masiva de datos con validación automática
- **Ejecución de Rutas**: Procesamiento multi-ruta con transacciones ACID
- **Auditoría Completa**: Historial de todas las operaciones
- **Filtros Avanzados**: Filtrado por estado, prioridad, ubicación, fecha
- **Autenticación**: Session-based y Token-based
- **Paginación Automática**: 50 registros por página (configurable)

### Características técnicas
- **Arquitectura Modular**: Domain-Driven Design (DDD)
- **Service Layer**: Lógica de negocio desacoplada
- **Repository Pattern**: Acceso a datos optimizado
- **Validación Multi-nivel**: Aplicación, negocio y base de datos
- **Manejo Estandarizado de Errores**: Respuestas API consistentes
- **Documentación Swagger**: OpenAPI 3.0 y Swagger UI
- **Tests Automatizados**: Tests unitarios e integración
- **Logging Estructurado**: Niveles de log configurables
- **Soporte CORS**: Configuración por entorno

### DevOps
- **Docker Multi-stage**: Imágenes optimizadas para producción
- **Docker Compose**: Stacks de desarrollo y producción
- **Nginx Reverse Proxy**: Pre-configurado
- **PostgreSQL 15**: Soporte de schema personalizado
- **Gunicorn**: Servidor WSGI de producción
- **Health Checks**: Monitoreo de servicios

---

## Casos de uso

1. **Importar Rutas**: Datos Excel → Validación → Base de Datos
2. **Ejecutar Rutas**: Procesar múltiples rutas con auditoría
3. **Seguimiento de Estado**: Consultas de historial de ejecución completo
4. **Dashboard de Estadísticas**: Totales por estado y prioridad
5. **Integración con Sistemas**: API REST para servicios terceros

---

## Arquitectura

### Patron MTV de Django (Model-Template-View)

Este proyecto implementa el patron MTV estandar de Django con Domain-Driven Design:

| Componente MTV | Ubicacion | Responsabilidad |
|---|---|---|
| **Model** | domain/models.py | Entidades ORM y logica de dominio |
| **Template** | api/serializers.py | Serializacion JSON y validacion |
| **View** | api/views.py | Procesamiento de HTTP requests |

---

### Estructura Modular por Capas

```
logistics-route-management-api/
├── config/                          # Configuración Django central
│   ├── settings.py                 # Variables, apps, middleware
│   ├── urls.py                     # Rutas principales
│   ├── wsgi.py / asgi.py          # Servidores web
│   └── __init__.py
│
├── apps/routes/                     # Aplicacion principal
│   │
│   ├── domain/                      # MTV MODEL Layer
│   │   ├── models.py              # Hereda models.Model (Django)
│   │   │                           # Entidades ORM persistibles
│   │   ├── managers.py            # Custom QuerySets optimizados
│   │   └── __init__.py
│   │
│   ├── application/                 # DDD Application Layer
│   │   ├── services.py            # Casos de uso de negocio
│   │   ├── validators.py          # Reglas de validacion
│   │   └── __init__.py
│   │
│   ├── infrastructure/              # DDD Infrastructure Layer
│   │   ├── repositories.py        # Acceso a datos (Pattern)
│   │   └── __init__.py
│   │
│   ├── api/                         # MTV VIEW + TEMPLATE Layer
│   │   ├── views.py               # ViewSets (MTV VIEW)
│   │   │                           # Hereda ViewSet (DRF)
│   │   │                           # Procesa HTTP requests/responses
│   │   ├── serializers.py         # Serializers (MTV TEMPLATE)
│   │   │                           # Valida y serializa datos
│   │   ├── filters.py             # Filtros avanzados
│   │   ├── urls.py                # MTV URL Routing
│   │   │                           # Conecta URLs a ViewSets
│   │   └── __init__.py
│   │
│   ├── management/                  # 🟣 COMANDOS PERSONALIZADOS
│   │   └── commands/
│   │       └── init_data.py       # Cargar datos iniciales
│   │
│   ├── tests/                       # 🔴 TESTS
│   │   ├── test_api.py            # Tests de API
│   │   └── __init__.py
│   │
│   ├── exceptions.py               # Excepciones personalizadas
│   ├── apps.py                     # Configuración de app
│   └── __init__.py
│
├── .vscode/                         # Configuración IDE
│   ├── settings.json               # Python, Black, flake8
│   └── launch.json                 # Debug configurado
│
├── manage.py                        # CLI de Django
├── requirements.txt                 # Dependencias Python
├── .env / .env.example             # Variables de entorno
│
├── docker-compose.yml              # Stack desarrollo
├── docker-compose.prod.yml         # Stack producción
├── Dockerfile                      # Imagen Docker
├── nginx.conf                      # Configuración Nginx
│
├── setup.sh / setup.bat            # Scripts setup automático
├── Makefile                        # Comandos útiles
│
└── DOCUMENTACIÓN/
    ├── README.md                   # Este archivo
    ├── QUICK_START.md              # Inicio 5 minutos
    ├── INSTALL.md                  # Instalación detallada
    ├── STRUCTURE.md                # Estructura explicada
    └── CONTRIBUTING.md             # Cómo contribuir
```

### 🏗️ Flujo MTV (Ciclo Completo)

**REQUEST:**
- CLIENT -> [URL] urls.py -> [VIEW] views.py -> [TEMPLATE] serializers.py
- -> [SERVICE] services.py -> [MODEL] models.py -> [DATABASE] PostgreSQL

**RESPONSE:**
- [DATABASE] -> [MODEL] -> [TEMPLATE] serializers.py -> [VIEW] -> CLIENT

**Conponentes MTV Implementados:**
1. **URL**: Rutas en urls.py (Django Router)
2. **VIEW**: ViewSets en views.py (Django REST Framework)
3. **MODEL**: Modelos ORM en models.py (Django models.Model)
4. **TEMPLATE**: Serializers en serializers.py (DRF Serializers)

**Complementado con DDD:**
- APPLICATION LAYER: Logica de negocio y validaciones
- INFRASTRUCTURE LAYER: Acceso a datos y repositories

### Principios de Diseño

- **MTV Pattern**: Patron estandar de Django (Model-Template-View)
- **Domain-Driven Design**: Modelos ricos en dominio
- **Separation of Concerns**: Cada capa responsabilidad unica
- **Repository Pattern**: Abstraccion de acceso a datos
- **Service Layer**: Logica desacoplada de persistencia
- **SOLID Principles**: Codigo mantenible y testeable
- **Clean Code**: Independencia de frameworks externos

---

## MTV en Endpoints REST

### Ejemplo de Implementacion MTV Completa: GET /routes/

**1. URL Routing (MTV Entry)**
```python
# apps/routes/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # MTV URL -> View
]
```

**2. VIEW: Procesa HTTP + Orquesta**
```python
# apps/routes/api/views.py
from rest_framework.viewsets import ModelViewSet
from .serializers import RouteSerializer
from ..application.services import RouteService

class RouteViewSet(ModelViewSet):
    # MTV VIEW: Procesa requests HTTP
    queryset = Route.objects.all()
    serializer_class = RouteSerializer  # MTV TEMPLATE

    def list(self, request):
        # GET /routes/ -> aqui se procesa
        service = RouteService()
        routes = service.get_all_routes()

        # Serializar respuesta (MTV TEMPLATE)
        serializer = self.serializer_class(routes, many=True)
        return Response(serializer.data)  # JSON Response
```

**3. MODEL: Entidad Persistible**
```python
# apps/routes/domain/models.py
from django.db import models

class Route(models.Model):
    # MTV MODEL: Hereda models.Model (Django)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.IntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
```

**4. TEMPLATE: Serializa JSON**
```python
# apps/routes/api/serializers.py
from rest_framework import serializers
from ..domain.models import Route

class RouteSerializer(serializers.ModelSerializer):
    # MTV TEMPLATE: Convierte Model <-> JSON
    class Meta:
        model = Route
        fields = ['id', 'origin', 'destination', 'distance_km',
                  'priority', 'status', 'created_at']

    def validate(self, data):
        # MTV TEMPLATE: Valida datos entrada
        if data['distance_km'] <= 0:
            raise serializers.ValidationError("Distance must be > 0")
        return data
```

**Ciclo MTV en esta solicitud GET /routes/:**
1. URL: urls.py enruta a ViewSet
2. VIEW: viewset.list() procesa request
3. TEMPLATE: serializer deserializa query
4. MODEL: Route.objects.all() consulta BD
5. TEMPLATE: serializer serializa a JSON
6. VIEW: Response retorna JSON al cliente

---

## Validación MTV + DDD

### Scripts de Validación Automática

Este proyecto incluye scripts Python para validar que la estructura MTV y DDD está correctamente implementada:

```bash
# Validar estructura MTV + DDD
python validate_structure.py

# Output esperado:
# ✓ Total Checks: 59
# ✓ Passed: 59
# ✓ Success Rate: 100.0%
```

**Validaciones Incluidas:**

✅ **MTV Pattern**
- Model layer (domain/models.py) hereda models.Model
- Template layer (api/serializers.py) usa ModelSerializer
- View layer (api/views.py) usa ViewSet
- URL routing correcto con DefaultRouter

✅ **DDD Layers**
- Domain layer con modelos y managers
- Application layer con servicios y validadores
- Infrastructure layer con repositorios
- Presentation layer con views y serializers

✅ **Django Configuration**
- settings.py correctamente configurado
- urls.py con enrutamiento correcto
- INSTALLED_APPS con todas las apps

✅ **Code Quality**
- Sintaxis Python válida
- Imports correctos
- Estructura de directorios

✅ **Documentation**
- README con MTV documentado
- Guides de instalación y uso
- Contributing guide incluida

**Reporte Detallado:** Ver [VALIDATION_REPORT.md](VALIDATION_REPORT.md)

---

## Stack Técnico

| Componente | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.10+ | Lenguaje base |
| **Django** | 5.0 | Framework web |
| **DRF** | 3.14 | API REST |
| **PostgreSQL** | 12+ | Base de datos |
| **Pandas** | 2.1 | Procesamiento Excel |
| **Gunicorn** | 21.2 | Servidor WSGI producción |
| **Nginx** | Latest | Reverse Proxy |
| **Docker** | Latest | Containerización |

---

## Instalación

### Requisitos Previos

- **Python** 3.10 o superior
- **PostgreSQL** 12 o superior
- **pip** o **poetry** para gestión de paquetes
- **Docker + Compose** (opcional, para containerización)
- **Git** para control de versiones

### Opción 1: Instalación Local Completa

#### Clonar Repositorio

```bash
git clone https://github.com/josetresdev/logistics-route-management-api.git
cd logistics-route-management-api
```

#### Crear Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

#### Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Configurar Base de Datos

**Crear base de datos en PostgreSQL:**

```sql
CREATE DATABASE logistics;
CREATE SCHEMA logistics;
```

O desde terminal:

```bash
# Linux / macOS
createdb -U postgres logistics

# Windows (con PostgreSQL instalado)
psql -U postgres -c "CREATE DATABASE logistics;"
psql -U postgres -d logistics -c "CREATE SCHEMA logistics;"
```

#### Configurar Variables de Entorno

Copiar `.env.example` a `.env`:

```bash
cp .env.example .env
```

Editar `.env` con tus valores:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-segura-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=logistics
DB_USER=postgres
DB_PASSWORD=tu-password-postgres
DB_HOST=localhost
DB_PORT=5432
DB_SCHEMA=logistics

SERVER_PORT=8000
SERVER_HOST=0.0.0.0
```

#### Aplicar Migraciones

```bash
python manage.py migrate
```

#### Cargar Datos Iniciales

```bash
python manage.py init_data
```

Carga:
- Estados de rutas (PENDING, IN_PROGRESS, COMPLETED, FAILED)
- Niveles de prioridad (1-4)
- Ubicaciones geográficas de ejemplo (Santiago, Valparaíso, etc)

#### Crear Superusuario (Admin)

```bash
python manage.py createsuperuser
```

Ingresar datos:
```
Username: admin
Email: admin@example.com
Password: admin123 (cambiar en producción)
```

#### Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

#### Iniciar Servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

El servidor está corriendo en **http://localhost:8000**

---

### Opción 2: Docker Compose (Recomendado)

#### Clonar Repositorio

```bash
git clone https://github.com/josetresdev/logistics-route-management-api.git
cd logistics-route-management-api
```

#### Iniciar Stack

```bash
# Construir imágenes
docker-compose build

# Levantar servicios
docker-compose up
```

Se inician automáticamente:
- PostgreSQL 15
- Django (Gunicorn)
- Migraciones
- Superusuario (admin/admin123)

#### Acceder

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

#### Ver Logs

```bash
docker-compose logs -f web  # Logs del API
docker-compose logs -f db   # Logs de BD
```

#### Detener

```bash
docker-compose down
```

---

### Opción 3: Producción con Docker + Nginx

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Stack:
- PostgreSQL 15 persistente
- Django + Gunicorn (4 workers)
- Nginx Reverse Proxy
- Health checks automatizados

---

## Uso y Endpoints

### Acceso a la Aplicación

Una vez ejecutando (puerto por defecto 8000):

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **API REST** | http://localhost:8000/api/ | Autenticación requerida |
| **Swagger UI** | http://localhost:8000/api/docs/ | Autenticación requerida |
| **ReDoc** | http://localhost:8000/api/redoc/ | Autenticación requerida |
| **OpenAPI Schema** | http://localhost:8000/api/schema/ | Público |
| **Admin Django** | http://localhost:8000/admin/ | admin/admin123 |

### Autenticación

**Obtener Token (si TokenAuth está habilitado):**

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Usar Token en Requests:**

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/routes/
```

---

### Endpoints REST Completos

#### Rutas

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| **GET** | `/api/routes/` | Listar todas rutas con paginación | Requerida |
| **POST** | `/api/routes/` | Crear nueva ruta | Requerida |
| **GET** | `/api/routes/{id}/` | Obtener detalles de ruta | Requerida |
| **PUT** | `/api/routes/{id}/` | Actualizar ruta completa | Requerida |
| **PATCH** | `/api/routes/{id}/` | Actualización parcial | Requerida |
| **DELETE** | `/api/routes/{id}/` | Eliminar ruta | Requerida |
| **POST** | `/api/routes/execute/` | Ejecutar múltiples rutas | Requerida |
| **POST** | `/api/routes/import_routes/` | Importar desde Excel | Requerida |
| **GET** | `/api/routes/{id}/execution_history/` | Historial de ejecución | Requerida |
| **GET** | `/api/routes/statistics/` | Estadísticas globales | Requerida |

#### Catálogos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| **GET** | `/api/route-statuses/` | Estados de rutas |
| **GET** | `/api/priorities/` | Niveles de prioridad |
| **GET** | `/api/locations/` | Ubicaciones geográficas |
| **GET** | `/api/execution-logs/` | Registros de ejecución |
| **GET** | `/api/import-batches/` | Lotes de importación |

---

### Ejemplos de Requests

#### Listar Rutas con Filtros

```bash
# Todas las rutas
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/routes/

# Filtrar por estado
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/routes/?status=PENDING"

# Filtrar por prioridad
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/routes/?priority=3"

# Filtrar por fecha
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/routes/?created_after=2024-01-01&created_before=2024-12-31"

# Buscar por ubicación
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/routes/?search=Santiago"

# Ordenar
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/routes/?ordering=-created_at"
```

#### Crear Ruta

```bash
curl -X POST http://localhost:8000/api/routes/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": 1,
    "destination": 2,
    "distance_km": 150.50,
    "priority": 2,
    "status": 1,
    "time_window_start": "2024-03-01T08:00:00Z",
    "time_window_end": "2024-03-01T18:00:00Z"
  }'
```

#### Ejecutar Rutas

```bash
curl -X POST http://localhost:8000/api/routes/execute/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "route_ids": [1, 2, 3]
  }'
```

#### Importar desde Excel

```bash
curl -X POST http://localhost:8000/api/routes/import_routes/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@routes.xlsx" \
  -F "batch_name=Lote Febrero 2024"
```

#### Ver Historial de Ejecución

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/routes/1/execution_history/
```

#### Estadísticas Globales

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/routes/statistics/
```

---

### Respuestas Estandarizadas

**Éxito (200 OK):**

```json
{
  "data": {
    "id": 1,
    "origin": 1,
    "destination": 2,
    "distance_km": 150.50,
    "status": "PENDING",
    "created_at": "2024-02-28T10:30:00Z"
  },
  "errors": null,
  "status": 200
}
```

**Error (400 Bad Request):**

```json
{
  "data": null,
  "errors": {
    "field_name": ["Error description"]
  },
  "status": 400
}
```

**Error (500 Error Interno del Servidor):**

```json
{
  "data": null,
  "errors": {
    "detail": "Internal server error"
  },
  "status": 500
}
```

---

## Modelos de Datos

### Relación de Tablas

```
geographic_locations ◄─┐
                        ├── routes
route_status ◄──────────┤
priority_catalog ◄──────┤
import_batches ◄────────┘
                    │
                    └──► execution_logs
```

### Tabla: routes

```python
class Route(models.Model):
    id: BigAutoField (PK)
    origin: FK → GeographicLocation
    destination: FK → GeographicLocation
    distance_km: Decimal(10,2)
    priority: FK → PriorityCatalog
    time_window_start: DateTime
    time_window_end: DateTime
    status: FK → RouteStatus
    batch: FK → ImportBatch (nullable)
    created_at: DateTime
    updated_at: DateTime
```

### Tabla: route_status

```python
class RouteStatus(models.Model):
    code: CharField(30)               # PENDING, IN_PROGRESS, COMPLETED, FAILED
    description: CharField(100)
    created_at: DateTime
```

### Tabla: priority_catalog

```python
class PriorityCatalog(models.Model):
    level: Integer                    # 1=Baja, 2=Normal, 3=Alta, 4=Crítica
    description: CharField(100)
    created_at: DateTime
```

### Tabla: geographic_locations

```python
class GeographicLocation(models.Model):
    name: CharField(150)              # Santiago Centro, Valparaíso, etc
    address: TextField
    latitude: Decimal(9,6)
    longitude: Decimal(9,6)
    created_at: DateTime
```

### Tabla: import_batches

```python
class ImportBatch(models.Model):
    filename: CharField(255)
    total_records: Integer
    valid_records: Integer
    invalid_records: Integer
    status: CharField()               # PENDING, PROCESSING, COMPLETED, FAILED
    created_at: DateTime
    updated_at: DateTime
```

### Tabla: execution_logs

```python
class ExecutionLog(models.Model):
    route: FK → Route
    execution_time: DateTime
    result: CharField()               # SUCCESS, FAILURE, PENDING
    message: TextField
    execution_ms: Integer (nullable)  # Duración en milisegundos
    created_at: DateTime
```

---

## Testing

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test apps.routes

# Test específico
python manage.py test apps.routes.tests.test_api.RouteAPITestCase

# Con verbosidad
python manage.py test apps.routes -v 2

# Con cobertura
coverage run --source='apps' manage.py test apps.routes
coverage report
coverage html  # Genera reporte visual
```

### Estructura de Tests

```
apps/routes/tests/
├── test_api.py              # Tests de endpoints REST
├── test_services.py         # Tests de servicios de negocio
├── test_repositories.py     # Tests de acceso a datos
└── test_validators.py       # Tests de validaciones
```

---

## Docker

### Desarrollo

```bash
# Build e iniciar
docker-compose build
docker-compose up

# Ver logs solamente
docker-compose logs -f web

# Ejecutar comando en contenedor
docker-compose exec web python manage.py createsuperuser

# Detener
docker-compose down

# Limpiar todo
docker-compose down -v
```

### Production

```bash
# Build
docker-compose -f docker-compose.prod.yml build

# Levantar
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Detener
docker-compose -f docker-compose.prod.yml down
```

Stack Producción:
- PostgreSQL 15 (persistente)
- Django + Gunicorn (4 workers)
- Nginx Reverse Proxy
- Health checks
- Logs centralizados

---

## Documentación

### Documentos Incluidos

| Archivo | Contenido |
|---------|----------|
| [README.md](README.md) | Este archivo |
| [QUICK_START.md](QUICK_START.md) | Inicio rápido en 5 minutos |
| [INSTALL.md](INSTALL.md) | Instalación detallada |
| [STRUCTURE.md](STRUCTURE.md) | Explicación de estructura |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Cómo contribuir |

### Documentación API

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

## Comandos Útiles

### Makefile (en Linux/Mac)

```bash
make help                 # Ver todos los comandos
make install              # Instalar dependencias
make run                  # Iniciar servidor
make migrate              # Aplicar migraciones
make superuser            # Crear admin
make test                 # Ejecutar tests
make lint                 # Validar código
make clean                # Limpiar caché
```

### Comandos de Gestión Django

```bash
# Servidor
python manage.py runserver 0.0.0.0:8000

# Migraciones
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --fake-initial

# Base de Datos
python manage.py shell
python manage.py dbshell

# Tests
python manage.py test apps.routes
python manage.py test apps.routes -v 2

# Datos
python manage.py init_data
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

# Mantenimiento
python manage.py check
python manage.py collectstatic
python manage.py createsuperuser
```

### Git Útil

```bash
git status
git add .
git commit -m "feat: descripción del cambio"
git push origin main
git log --oneline
git branch

# Revertir cambios
git checkout -- archivo.py
git reset --hard
```

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'django'"

```bash
# Verificar que virtual environment esté activado
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Error: "could not connect to server: Connection refused"

PostgreSQL no está corriendo:

```bash
# Windows
Get-Service -Name postgresql-x64-15 | Start-Service

# Linux
sudo systemctl start postgresql

# macOS
brew services start postgresql
```

### Error: "database "logistics" does not exist"

```bash
# Crear base de datos
createdb -U postgres logistics

# O en psql
psql -U postgres
CREATE DATABASE logistics;
CREATE SCHEMA logistics;
```

### Error: "Port 8000 already in use"

```bash
# Usar puerto diferente
python manage.py runserver 0.0.0.0:8001

# O matar proceso
# Linux/Mac:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Migraciones pendientes

```bash
python manage.py migrate

# Resetear migraciones (CUIDADO: borra datos)
python manage.py migrate apps.routes zero
python manage.py migrate
```

---

## Seguridad en Producción

### Checklist de Seguridad

- [ ] `DEBUG=False` en `.env`
- [ ] Generar `SECRET_KEY` fuerte
- [ ] Actualizar `ALLOWED_HOSTS`
- [ ] Configurar `CORS_ALLOWED_ORIGINS` correcto
- [ ] Verificar contraseña de PostgreSQL fuerte
- [ ] Usar HTTPS/SSL
- [ ] Configurar headers de seguridad
- [ ] Revisar permisos de archivos
- [ ] Configurar backups automáticos
- [ ] Implementar rate limiting

### Generar SECRET_KEY Segura

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Variables Producción

```env
DEBUG=False
SECRET_KEY=generated-strong-key-here
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com
DB_PASSWORD=very-strong-password-here
```

---

## Despliegue

### Heroku

```bash
heroku login
heroku create tu-app-name
git push heroku main
heroku config:set DEBUG=False
heroku run python manage.py migrate
```

### AWS EC2

```bash
# Instalar dependencias
sudo apt install python3-pip python3-venv postgresql postgresql-contrib

# Setup aplicación
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Gunicorn + Systemd + Nginx
```

### DigitalOcean

Usar App Platform Docker - conectar repositorio y desplegar automáticamente

---

## Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/nombre-feature`
3. Commit cambios: `git commit -m "feat: descripción"`
4. Push: `git push origin feature/nombre-feature`
5. Crear Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

### Desarrollo Local

```bash
# Instalar dependencias dev
pip install black flake8 pytest pytest-cov

# Formatear código
black apps config

# Validar
flake8 apps config --max-line-length=100

# Tests
pytest apps/routes/tests/
```

---

## Licencia

MIT License - Libre para uso comercial y personal

---

## Autor

Desarrollado por **Equipo de Desarrollo Falabella**

---

## Contacto

- Email: dev@falabella.com
- Issues: [GitHub Issues](https://github.com/josetresdev/logistics-route-management-api/issues)
- Docs: [Project Wiki](https://github.com/josetresdev/logistics-route-management-api/wiki)

---

## Checklist Final

Antes de usar en producción:

- [x] Clonar repositorio
- [x] Instalar dependencias
- [x] Configurar base de datos
- [x] Crear superusuario
- [x] Cargar datos iniciales
- [x] Ejecutar tests
- [x] Revisar documentación
- [x] Configurar variables de seguridad
- [x] Hacer backup
- [x] Desplegar

---

Gracias por usar Logistics Route Management API.

Para preguntas o reportar bugs, abre un issue en GitHub.

**Última actualización:** Febrero 28, 2026
