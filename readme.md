# Logistics Route Management API

Sistema de gestión y optimización de rutas de logística con Django REST Framework.

## 📋 Requisitos Previos

- Python 3.10+
- PostgreSQL 16 (vía Docker)
- Docker & Docker Compose
- pip

## 🚀 Quick Start

### 1. Clonar el Repositorio

```bash
git clone https://github.com/josetresdev/logistics-route-management-api.git
cd logistics-route-management-api
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Levantar la Base de Datos con Docker

```bash
docker-compose up -d postgres
```

Esto levantará PostgreSQL en `localhost:5432` con:
- **Database**: logistics
- **Usuario**: postgres
- **Contraseña**: postgres
- **Schema**: logistics (creado automáticamente)
- **Datos iniciales**: Se importan automáticamente desde `db/init.sql`

### 4. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Las variables ya están configuradas para conectar a la BD local:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=logistics
DB_USER=postgres
DB_PASSWORD=postgres
```

### 5. Ejecutar Migraciones de Django

```bash
python manage.py migrate
```

### 6. Iniciar el Servidor de Desarrollo

```bash
python manage.py runserver 0.0.0.0:8000
```

El servidor estará disponible en: **http://localhost:8000**

## 📡 Endpoints Principales

```
GET    /api/routes/              - Listar todas las rutas
POST   /api/routes/              - Crear nueva ruta
GET    /api/routes/{id}/         - Obtener detalle de ruta
PUT    /api/routes/{id}/         - Actualizar ruta
DELETE /api/routes/{id}/         - Eliminar ruta

GET    /api/import-batch/        - Historial de importaciones
POST   /api/import-batch/upload/ - Importar rutas desde Excel

GET    /api/execution-log/       - Registro de ejecuciones
```

## 🏗️ Estructura del Proyecto

```
.
├── apps/
│   └── routes/
│       ├── domain/          # Modelos ORM (MTV Model)
│       ├── application/     # Lógica de negocio (DDD)
│       ├── infrastructure/  # Acceso a datos
│       └── api/             # Serializers y Views (MTV View/Template)
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

## 📊 Arquitectura

El proyecto implementa dos patrones de arquitectura complementarios:

### MTV (Model-Template-View)

- **Model** (`apps/routes/domain/models.py`): Modelos ORM de Django
- **Template** (`apps/routes/api/serializers.py`): Serialización JSON (DRF)
- **View** (`apps/routes/api/views.py`): Vistas REST (ViewSets)

### DDD (Domain-Driven Design)

- **Domain Layer**: Modelos, entidades de negocio
- **Application Layer**: Servicios, casos de uso
- **Infrastructure Layer**: Repositorios, acceso a datos
- **API Layer**: Controllers REST, serializers

## 🔧 Configuración de la Base de Datos

### Schema Principal: `logistics`

**Tablas**:
- `route_status` - Catálogo de estados
- `priority_catalog` - Catálogo de prioridades
- `geographic_locations` - Ubicaciones geográficas
- `routes` - Rutas principales
- `route_payload` - Payloads JSON de rutas
- `execution_logs` - Registro de ejecuciones
- `import_batches` - Historial de importaciones

### Constraints Principales

```sql
-- Validación de ventana de tiempo
CHECK (time_window_start < time_window_end)

-- Validación de coordenadas
CHECK (latitude BETWEEN -90 AND 90)
CHECK (longitude BETWEEN -180 AND 180)

-- Distancia positiva
CHECK (distance_km > 0)

-- Unicidad de combinación de ruta
UNIQUE (origin, destination, time_window_start, time_window_end)
```

## 🐳 Docker

### Levantar BD con Docker Compose

```bash
docker-compose up -d postgres
```

Espera a que PostgreSQL esté listo. Puedes verificar con:

```bash
docker-compose logs postgres
```

### Detener los Servicios

```bash
docker-compose down
```

### Ver Logs

```bash
docker-compose logs -f postgres
```

## 📦 Dependencias Principales

- **Django 5.0.1** - Framework web
- **djangorestframework 3.14.0** - API REST
- **psycopg2-binary 2.9.10** - Driver PostgreSQL
- **pandas 2.2.3** - Procesamiento de datos
- **drf-spectacular 0.27.0** - Documentación automática de API
- **gunicorn 21.2.0** - Servidor WSGI producción

Ver `requirements.txt` para lista completa.

## 🔍 Monitoreo y Debugging

### Ver Estado de Servicios Docker

```bash
docker-compose ps
```

### Conectar a PostgreSQL

```bash
psql -h localhost -U postgres -d logistics
```

### Ver Migraciones de Django

```bash
python manage.py showmigrations
```

### Crear Superusuario

```bash
python manage.py createsuperuser
```

## 🚢 Despliegue en Producción

```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Requisitos antes de producción**:

1. Cambiar `SECRET_KEY` en `.env`
2. Cambiar contraseña de PostgreSQL
3. Configurar `DEBUG=False`
4. Configurar `ALLOWED_HOSTS` correctamente
5. Guardar credenciales en variables de entorno seguras
6. Configurar SSL/HTTPS

## 🤝 Equipo

Equipo de Desarrollo Falabella

## 📄 Licencia

Privada - Falabella

## 📞 Soporte

Para reportar issues o sugerencias, contacta al equipo de desarrollo.

---

**Última actualización**: Febrero 2026
**Versión**: 1.0.0 Producción
