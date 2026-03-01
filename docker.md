# 🗑️ COMANDOS DE LIMPIEZA - Docker & Base de Datos

## ⚠️ IMPORTANTE
Estos comandos **BORRAN TODO**: contenedores, volúmenes, datos de la BD, etc.
Solo usa si quieres empezar desde cero con las tablas iniciales del `init.sql`.

---

## 1️⃣ LIMPIEZA COMPLETA (Recomendado)

### Opción A: Script Automático (Windows)
```bash
# Ejecuta todo automáticamente
./cleanup-docker.bat
```

### Opción B: Script Automático (PowerShell)
```powershell
# Con colores y mejor formato
./cleanup-docker.ps1
```

### Opción C: Comandos Manuales (Linux/Mac/Windows PowerShell)
```bash
# Detiene y borra contenedores
docker-compose down

# Borra volúmenes (ELIMINA BASE DE DATOS COMPLETA)
docker-compose down -v

# Limpia contenedores huérfanos
docker container prune -f

# Limpia volúmenes huérfanos
docker volume prune -f

# Limpia redes huérfanas
docker network prune -f
```

---

## 2️⃣ SOLO BAJAR CONTENEDORES (sin borrar datos)
```bash
docker-compose down
```

---

## 3️⃣ REINICIAR COMPLETAMENTE (limpieza + startup)

### Con Script Automático
```bash
# Windows CMD
cleanup-docker.bat && docker-compose up -d

# PowerShell
./cleanup-docker.ps1; docker-compose up -d
```

### Con Comandos Manuales
```bash
docker-compose down -v && docker-compose up -d
```

---

## 4️⃣ VER ESTADO DE DOCKER
```bash
# Ver contenedores activos
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f logistics-django
docker-compose logs -f logistics-postgres
```

---

## 5️⃣ LIMPIAR SOLO LA BASE DE DATOS (sin bajar Docker)
```bash
# SOLO borra el volumen de Postgres
docker volume rm logistics-route-management-api_postgres-data

# Luego reinicia Docker para que init.sql se ejecute
docker-compose restart logistics-postgres
```

---

## 📋 QUÉ HACE init.sql AHORA

El archivo `db/init.sql` ha sido actualizado y contiene:

✅ **Tablas de Django** (auth, tokens, sesiones)
✅ **Tablas personalizadas** (routes, locations, etc.)
✅ **Estados iniciales** (route_status con 7 estados)
✅ **Usuario admin** (usuario: `admin`, contraseña: `admin123`)

Cuando Docker sube, **init.sql se ejecuta automáticamente** en Postgres.

---

## 🚀 WORKFLOW COMPLETO

```bash
# 1. Limpiar todo
docker-compose down -v

# 2. Iniciar Docker (ejecuta init.sql automáticamente)
docker-compose up -d

# 3. Verificar que está todo listo
docker-compose ps

# 4. Ver logs
docker-compose logs -f

# 5. Probar endpoint (desde otra terminal)
curl -X GET http://localhost:8000/api/routes/
```

---

## ✅ DESPUÉS DE LIMPIAR Y REINICIAR

Tendrá:
- ✓ Base de datos vacía pero con estructura completa
- ✓ 7 estados de ruta disponibles
- ✓ Usuario admin disponible para login
- ✓ Token auth listo para usar
- ✓ Listo para importar dataset.xlsx

---

## 🔑 AUTENTICACIÓN

```bash
# Obtener token de autenticación
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Respuesta (example)
{"token": "8b57ab78b769b0bb358c60b2eef025c6efc895a2"}

# Usar token en requests
curl -X POST http://localhost:8000/api/routes/import/ \
  -H "Authorization: Token 8b57ab78b769b0bb358c60b2eef025c6efc895a2" \
  -F "file=@dataset.xlsx"
```

---

## 📝 NOTAS IMPORTANTES

1. **init.sql es la fuente de verdad**: Si cambias tablas en Django models, actualiza init.sql
2. **Las migraciones NO se usan**: Todo está en init.sql ahora
3. **Datos dentro del Docker**: Se pierden al hacer `down -v`
4. **Para desarrollo local**: Considera hacer `docker-compose down` sin `-v` para preservar datos
5. **Token hardcodeado**: El usuario admin se crea automáticamente en cada limpieza

---

## 🐛 TROUBLESHOOTING

### Docker no inicia
```bash
# Ver otros procesos usando puertos
netstat -ano | findstr :5432    # Postgres
netstat -ano | findstr :8000    # Django
```

### Base de datos corrupta
```bash
# Limpia solo Postgres
docker volume rm logistics-route-management-api_postgres-data
docker-compose restart logistics-postgres
```

### Ver si init.sql se ejecutó
```bash
docker-compose exec logistics-postgres psql -U postgres -d logistics -c "\dt logistics.*"
```
