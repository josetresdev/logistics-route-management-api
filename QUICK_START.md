# Guía de Inicio Rápido

Inicia tu API de Rutas Logísticas en minutos

---

## Opción 1: Windows

### Pasos Rápidos

```batch
# 1. Navegar a la carpeta del proyecto
cd logistics-route-management-api

# 2. Ejecutar setup
setup.bat

# 3. Activar virtual environment
venv\Scripts\activate

# 4. Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

Acceder a: http://localhost:8000/api/

---

## Opción 2: Linux / macOS

### Pasos Rápidos

```bash
# 1. Navegar a la carpeta del proyecto
cd logistics-route-management-api

# 2. Ejecutar setup
bash setup.sh

# 3. El script activa el ambiente automáticamente

# 4. Para inicios posteriores, activar ambiente
source venv/bin/activate

# 5. Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

Access at: http://localhost:8000/api/

---

## Option 3: Docker (Easiest)

Solo necesitas Docker instalado:

```bash
# Construir e iniciar
docker-compose up

# En otra terminal (para crear admin)
docker-compose exec web python manage.py createsuperuser
```

Access at: http://localhost:8000/api/

---

## First Steps in the API

### 1. Open Admin Panel
```
http://localhost:8000/admin/
Username: admin
Password: admin123
```

### 2. Load Initial Data
```bash
python manage.py init_data
```

Esto carga:
- Estados de rutas (PENDING, IN_PROGRESS, COMPLETED, FAILED)
- Niveles de prioridad (1-4)
- Ubicaciones geográficas de ejemplo

### 3. Explorar API
```
GET  http://localhost:8000/api/routes/
GET  http://localhost:8000/api/locations/
GET  http://localhost:8000/api/priorities/
```

### 4. Ver Documentación Interactiva
```
http://localhost:8000/api/docs/
```

---

## Primeros Endpoints para Probar

### Listar Rutas

```bash\ncurl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/routes/
```

### List Locations

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/locations/
```

### List Priorities

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/priorities/
```

---

## Useful Commands

### Ejecutar Tests
```bRun Tests
```bash
python manage.py test apps.routes
```

### View Environment Variables
```bash
cat .env
```

### Reset Database
```bash
# WARNING: Deletes all data
python manage.py flush
```

### Enter Django Shell
```bash
python manage.py shell
```

---

## Quick Troubleshooting\n\n### Error: \"ModuleNotFoundError: No module named 'django'\"
pip install -r requirements.txt
```

### Error: "ConnectionRefusedError" a PostgreSQL
```bash
# Verificar que PostgreSQL está corriendo
# Windows:\"ConnectionRefusedError\" to PostgreSQL
```bash
# Verify PostgreSQL is running
# Windows:
net start postgresql-x64-15

# Linux:
sudo systemctl start postgresql

# macOS:
brew services start postgresql
```

### Port 8000 in use
```bash
python manage.py runserver 0.0.0.0:8001
```

---

## Next Stepctura en INSTALL.md**
3. **Ver ejemplos de API en /api/docs/**
4. **Read documentation in README.md**
2. **Explore structure in INSTALL.md**
3. **View API examples in /api/docs/**
4. **Start importing routes from Excel**

---

## Validation

Verify everything works:

```bash
python manage.py check
```

Should show

---

¡Listo! Ya tenés tu API corriendo. 🎉
