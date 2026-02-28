# Guía de Instalación y Setup

Sistema de Gestión de Rutas Logísticas - Backend Django

---

## Requisitos Previos

- Python 3.10 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes Python)
- Docker y Docker Compose (opcional, para containerización)

---

### Instalación Local

#### 1. Clonar Repositorio

```bash
git clone https://github.com/josetresdev/logistics-route-management-api.git
cd logistics-route-management-api
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file in project root:

```bash
DEBUG=True
SECRET_KEY=super-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=logistics
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_SCHEMA=logistics

# Server
SERVER_PORT=8000
SERVER_HOST=0.0.0.0
```

### 5. Create PostgreSQL Database

**Windows (PowerShell):**
```powershell
psql -U postgres -c "CREATE DATABASE logistics;"
```

**Linux / macOS:**
```bash
createdb -U postgres logistics
```

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow interactive prompts:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (change in production)

### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 9. Start Server

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## API Access

Once server is running:

- **API Endpoints**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

**Admin Credentials:**
- Username: `admin`
- Password: `admin123` (as configured in step 7)

---

## Docker Installation

### Prerequisites

- Docker installed
- Docker Compose installed

### 1. Build Image

```bash
docker-compose build
```

### 2. Start Containers

```bash
docker-compose up
```

O en background:

```bash
docker-compose up -d
```

### 3. Apply Migrations (if not automatic)

```bash
docker-compose exec web python manage.py migrate
```

### 4. Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access API

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

### View Logs

```bash
docker-compose logs -f web
```

### Stop Containers

```bash
docker-compose down
```

---

## Useful Commands

### Using Make (if installed)

```bash
# View all available commands
make help

# Install dependencies
make install

# Run server
make run

# Run migrations
make migrate

# Create superuser
make superuser

# Ejecutar tests
make test

# Run linting
make lint

# Clean cache
make clean
```

### Comandos Django Directos

```bash
# Listar todas las URLs
python manage.py show_urls

# Inspect database
python manage.py dbshell

# Create migrations
python manage.py makemigrations

# View pending migrations
python manage.py showmigrations

# Ejecutar tests
python manage.py test apps.routes

# Interactive shell
python manage.py shell

# Validate configuration
python manage.py check
```

---

## PostgreSQL Schema

The project expects `logistics` schema to exist in PostgreSQL. If you need to create the schema manually:

```sql
CREATE SCHEMA logistics;
```

Los modelos Django mapearán automáticamente a esta schema con `search_path=logistics` configurado en settings.py.

---

## Data Structure

### Main Tables

1. **routes**: Rutas logísticas
2. **route_status**: Estados disponibles (PENDING, IN_PROGRESS, COMPLETED, FAILED)
3. **priority_catalog**: Niveles de prioridad (1-4)
4. **geographic_locations**: Ubicaciones geográficas
5. **import_batches**: Lotes de importación
6. **execution_logs**: Auditoría de ejecuciones

---

## Production Configuration

### Critical Variables for Production

```bash
DEBUG=False
SECRET_KEY=<generar-clave-segura>
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DB_PASSWORD=<contraseña-fuerte>
CORS_ALLOWED_ORIGINS=https://tu-dominio.com
```

### Generate Strong SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Deployment with Gunicorn

```bash
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log
```

---

## Testing

### Run All Tests

```bash
python manage.py test apps.routes
```

### Run Specific Tests

```bash
python manage.py test apps.routes.tests.test_views
python manage.py test apps.routes.tests.test_services
```

### With Coverage

```bash
coverage run --source='apps' manage.py test apps.routes
coverage report
coverage html  # Generate HTML report
```

---

## Troubleshooting

### Error: \"psycopg2.OperationalError: could not connect to server\"

Verify that PostgreSQL is running:

```bash
# Windows
Get-Service -Name postgresql-x64-15 | Start-Service

# Linux
sudo systemctl start postgresql

# macOS
brew services start postgresql
```

### Error: \"ModuleNotFoundError: No module named 'django'\"

Ensure virtual environment is activated and dependencies installed:

```bash
pip install -r requirements.txt
```

### Error in Migrations

```bash
# Reset migrations (WARNING: deletes data)
python manage.py migrate apps.routes zero
python manage.py migrate
```

### Port 8000 in Use

Change execution port:

```bash
python manage.py runserver 0.0.0.0:8001
```

---

## Additional Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

## Validate Installation

Run Django check command:

```bash
python manage.py check
```

Must show: `System check identified no issues (0 silenced).`

---

## Support

For issues or suggestions, create an issue on GitHub or contact the development team.
