# Estructura del Proyecto

Documentación completa de la estructura arquitectónica

---

## Árbol de Directorios

```
logistics-route-management-api/
├── config/                          ← Configuración Django central
│   ├── __init__.py
│   ├── settings.py                 ← Variables, INSTALLED_APPS, DB config
│   ├── urls.py                     ← Rutas principales
│   ├── asgi.py                     ← ASGI (async)
│   └── wsgi.py                     ← WSGI (sync/production)
│
├── apps/
│   └── routes/                      ← App principal de rutas
│       ├── domain/                  ← Capa de dominio
│       │   ├── __init__.py
│       │   ├── models.py           ← Modelos ORM (Route, RouteStatus, etc)
│       │   └── managers.py         ← Custom QuerySets y Managers
│       │
│       ├── application/             ← Lógica de negocio
│       │   ├── __init__.py
│       │   ├── services.py         ← RouteService, ImportService, ExecutionService
│       │   └── validators.py       ← Validaciones de negocio
│       │
│       ├── infrastructure/          ← Capa de persistencia
│       │   ├── __init__.py
│       │   └── repositories.py     ← RouteRepository, ExecutionRepository
│       │
│       ├── api/                     ← API REST
│       │   ├── __init__.py
│       │   ├── views.py            ← ViewSets (RouteViewSet, etc)
│       │   ├── serializers.py      ← Serializers (RouteSerializer, etc)
│       │   ├── filters.py          ← FilterSets personalizados
│       │   └── urls.py             ← Router y rutas
│       │
│       ├── management/              ← Comandos personalizados
│       │   ├── __init__.py
│       │   └── commands/
│       │       ├── __init__.py
│       │       └── init_data.py    ← Comando para cargar datos iniciales
│       │
│       ├── tests/                   ← Tests
│       │   ├── __init__.py
│       │   └── test_api.py         ← Tests de API
│       │
│       ├── __init__.py
│       ├── apps.py                 ← Configuración de app
│       └── exceptions.py           ← Excepciones personalizadas
│
├── .vscode/                         ← Configuración VS Code
│   ├── settings.json               ← Settings de Python, formateo
│   └── launch.json                 ← Configuración de debug
│
├── manage.py                        ← Punto de entrada Django
├── requirements.txt                 ← Dependencias Python
├── .env                            ← Variables de entorno (no commitear)
├── .env.example                    ← Ejemplo de .env
├── .gitignore                      ← Archivos a ignorar git
├── .dockerignore                   ← Archivos a ignorar Docker
│
├── Dockerfile                      ← Configuración Docker
├── docker-compose.yml              ← Compose para desarrollo
├── docker-compose.prod.yml         ← Compose para producción con nginx
├── nginx.conf                      ← Configuración nginx
│
├── README.md                        ← Documentación principal
├── INSTALL.md                      ← Guía de instalación detallada
├── QUICK_START.md                  ← Inicio rápido
├── CONTRIBUTING.md                ← Cómo contribuir
├── STRUCTURE.md                    ← Este archivo
├── Makefile                        ← Comandos útiles
├── setup.sh                        ← Script setup Linux/Mac
└── setup.bat                       ← Script setup Windows
```

---

## Modelos ORM (Capa de Dominio)

### Route (Principal)
```python
- id: BigAutoField (PK)
- origin: FK → GeographicLocation
- destination: FK → GeographicLocation
- distance_km: DecimalField
- priority: FK → PriorityCatalog
- time_window_start: DateTimeField
- time_window_end: DateTimeField
- status: FK → RouteStatus
- batch: FK → ImportBatch (nullable)
- created_at: DateTimeField
- updated_at: DateTimeField
```

### RouteStatus (Catálogo)
```python
- id
- code: CharField (PENDING, IN_PROGRESS, COMPLETED, FAILED)
- description
- created_at
```

### PriorityCatalog
```python
- id
- level: IntegerField (1-4)
- description
- created_at
```

### GeographicLocation
```python
- id
- name
- address
- latitude
- longitude
- created_at
```

### ImportBatch
```python
- id
- filename
- total_records
- valid_records
- invalid_records
- status
- created_at
- updated_at
```

### ExecutionLog (Auditoría)
```python
- id
- route: FK → Route
- execution_time
- result (SUCCESS, FAILURE, PENDING)
- message
- execution_ms
- created_at
```

---

## Architecture Layers

### Domain Layer (`domain/`)
**Responsibility**: ORM models and domain logic

Archivos:
- `models.py`: Defines data structure
- `managers.py`: Custom QuerySets for optimizations

Ejemplo:
```python
class Route(models.Model):
    origin = models.ForeignKey(GeographicLocation, ...)
    # ... otros campos

    class Meta:
        db_table = "routes"
        managed = False  # La tabla existe en SQL
```

### Application Layer (`application/`)
**Responsibility**: Business logic

Archivos:
- `services.py`: Use cases (RouteService, ImportService)
- `validators.py`: Validation rules

Ejemplo:
```python
class RouteService:
    @staticmethod
    @transaction.atomic
    def execute_routes(route_ids):
        # Lógica compleja de ejecución con transacciones
```

### Infrastructure Layer (`infrastructure/`)
**Responsibility**: Data access

Archivos:
- `repositories.py`: Patrones de acceso a datos

Ejemplo:
```python
class RouteRepository:
    @staticmethod
    def get_by_status(status_code):
        return Route.objects.filter(status__code=status_code)
```

### API Layer (`api/`)
**Responsibility**: REST exposure

Archivos:
- `views.py`: REST View Sets
- `serializers.py`: JSON Serialization/Deserialization
- `filters.py`: Advanced filters
- `urls.py`: Routes

Ejemplo:
```python
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteDetailSerializer

    @action(detail=False, methods=["post"])
    def execute(self, request):
        # Endpoint POST /routes/execute/
```

---

## HTTP Request Flow

```
1. Cliente: GET /api/routes/?status=PENDING

2. URLs (apps/routes/api/urls.py)
   └─> Router mapea a RouteViewSet.list()

3. Views (apps/routes/api/views.py)
   ├─> Autent ICATION
   ├─> Permisos
   └─> GET queryset

4. Repositorio / QuerySet (infrastructure/)
   └─> Route.objects.filter(status__code="PENDING")

5. Serializer (api/serializers.py)
   └─> Convierte modelos a JSON

6. Response:
   {
     "data": [...],
     "errors": null,
     "status": 200
   }
```

---

## Available Endpoints

### Routes
```
GET    /api/routes/                    - Listar rutas
POST   /api/routes/                    - Crear ruta
GET    /api/routes/{id}/               - Detalle
PUT    /api/routes/{id}/               - Actualizar
DELETE /api/routes/{id}/               - Eliminar
POST   /api/routes/execute/            - Ejecutar rutas
POST   /api/routes/import_routes/      - Importar Excel
GET    /api/routes/{id}/execution_history/ - Historial
GET    /api/routes/statistics/         - Estadísticas globales
```

### Catálogos
```
GET    /api/route-statuses/            - Estados
GET    /api/priorities/                - Prioridades
GET    /api/locations/                 - Ubicaciones
GET    /api/execution-logs/            - Logs de ejecución
GET    /api/import-batches/            - Lotes de importación
```

---

## 🐳 Docker

### Desarrollo
```bash
docker-compose up
```

Stack:
- PostgreSQL 15
- Django 5.0 (Gunicorn)
- DRF 3.14

### Producción
```bash
docker-compose -f docker-compose.prod.yml up
```

Stack:
- PostgreSQL 15
- Django 5.0 (Gunicorn)
- Nginx (Reverse Proxy)

---

## 🔐 Seguridad

- `ALLOWED_HOSTS`: Whitelist de hosts
- `DEBUG=False` en producción
- `SECRET_KEY`: Generada segura
- Autenticación: Session + Token
- CORS: Configurado en settings

---

## 📊 Base de Datos

**Schema**: `logistics`

Tablas:
- `routes`
- `route_status`
- `priority_catalog`
- `geographic_locations`
- `import_batches`
- `execution_logs`

**Configuración**:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "options": "-c search_path=logistics"
        }
    }
}
```

---

## 🧪 Testing

**Ubicación**: `apps/routes/tests/`

Cobertura:
- Tests unitarios
- Tests de API
- Tests de servicios

Ejecutar:
```bash
python manage.py test apps.routes
coverage run --source='apps' manage.py test
coverage report
```

---

## Main Dependencies

| Paquete | Versión | Propósito |
|---------|---------|----------|
| Django | 5.0 | Framework web |
| djangorestframework | 3.14 | API REST |
| psycopg2-binary | 2.9 | Driver PostgreSQL |
| pandas | 2.1 | Procesamiento Excel |
| drf-spectacular | 0.27 | Documentación OpenAPI |
| gunicorn | 21.2 | WSGI server producción |
| django-cors-headers | 4.3 | CORS handling |

---

## 🛠️ Comandos Útiles

### Django Manage
```bash
python manage.py runserver              # Servidor dev
python manage.py makemigrations          # Crear migrations
python manage.py migrate                 # Aplicar migrations
python manage.py createsuperuser         # Admin user
python manage.py shell                   # Shell interactivo
python manage.py test apps.routes        # Tests
python manage.py init_data               # Cargar datos iniciales
```

### Make
```bash
make help                 # Ver todos los comandos
make install              # Instalar dependencias
make run                  # Iniciar servidor
make migrate              # Migrations
make test                 # Tests
make lint                 # Linting
```

### Docker
```bash
docker-compose up         # Iniciar
docker-compose logs -f    # Logs
docker-compose exec ...   # Ejecutar comando en contenedor
docker-compose down       # Detener
```

---

## 📖 Variables de Entorno

Ver `.env.example` para todas las variables:

```bash
DEBUG                    # True/False
SECRET_KEY              # Clave secreta Django
ALLOWED_HOSTS           # Hosts permitidos
DB_*                    # Configuración BD
CORS_ALLOWED_ORIGINS    # Origins permitidos para CORS
```

---

## ✅ Validación del Proyecto

```bash
# Check de Django
python manage.py check

# Validación de estructura
ls apps/routes/domain/models.py
ls apps/routes/application/services.py
ls apps/routes/api/views.py

# Prueba de imports
python -c "from django.conf import settings; print('✓ Django configured')"
```

---

## 🎯 Próximos Pasos

1. Leer [QUICK_START.md](QUICK_START.md) para ejecutar rápidamente
2. Leer [INSTALL.md](INSTALL.md) para instalación completa
3. Revisar [README.md](README.md) para documentación de la API
4. Leer [CONTRIBUTING.md](CONTRIBUTING.md) para contribuir

---

¡Proyecto completamente estruturado y listo para desarrollo y producción! 🚀
