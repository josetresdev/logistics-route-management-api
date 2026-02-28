# Guía de Contribución

Gracias por tu interés en contribuir a **Logistics Route Management API**

---

## Código de Conducta

- Sé respetuoso con otros contribuyentes
- Mantén un ambiente de inclusión
- Reporta comportamientos inapropiados

---

## Cómo Contribuir

### 1. Fork y Clone el Repositorio

```bash
git clone https://github.com/josetresdev/logistics-route-management-api.git
cd logistics-route-management-api
```

### 2. Create a Branch for your Feature

```bash
git checkout -b feature/nombre-de-la-feature
```

### 3. Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pre-commit black flake8 pytest pytest-cov
```

### 4. Make Changes

- Follow the existing structure
- Keep code clean and well documented
- Add tests for new functionality

### 5. Run Tests

```bash
python manage.py test apps.routes
coverage run --source='apps' manage.py test apps.routes
coverage report
```

### 6. Run Linting

```bash
flake8 apps config --max-line-length=100
black apps config
```

### 7. Commit and Push

```bash
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/nombre-de-la-feature
```

### 8. Create Pull Request

- Go to GitHub and create PR
- Describe changes clearly
- Reference issues if applicable

---

## Code Structure

```
apps/routes/
├── domain/          # Modelos, lógica de dominio
├── application/     # Servicios, validadores
├── infrastructure/  # Repositorios, persistencia
├── api/             # Serializers, Views, URLs
└── tests/           # Tests unitarios
```

### Principles

1. **Separation of Responsibilities**: Each layer has specific purpose
2. **DRY (Don't Repeat Yourself)**: Avoid duplicate code
3. **SOLID**: Software design principles
4. **Documentation**: Docstring in classes and methods

---

## Code Style

### Python

- Use **Black** for formatting
- 100 characters maximum per line
- Descriptive names in English
- Docstrings in Google format

Example:

```python
def create_route(validated_data):
    """
    Create a new route with validations.

    Args:
        validated_data (dict): Validated route data

    Returns:
        Route: Created route instance

    Raises:
        InvalidRouteData: If data is not valid
    """
    return Route.objects.create(**validated_data)
```

### Commits

Use conventional format:

```
feat: add new import endpoint
fix: fix time window validation
docs: update README
test: add tests for RouteService
refactor: reorganize folder structure
chore: update dependencies
```

---

## Testing

### Requirements

- Minimum 80% coverage
- Tests for new features
- Tests for bug fixes

### Run Tests

```bash
# All tests
python manage.py test apps.routes

# Specific test
python manage.py test apps.routes.tests.test_views.RouteAPITestCase.test_routes_list_endpoint

# With coverage
coverage run --source='apps' manage.py test apps.routes
coverage report
coverage html  # Generate visual report
```

---

## 📝 Documentación

- Actualizar README si hay cambios en API
- Agregar docstrings en código
- Mantener INSTALL.md actualizado
- Documentar nuevos endpoints en API docs

---

## 🔒 Seguridad

- No comitear `.env` con secretos reales
- No compartir credenciales en PRs
- Reportar vulnerabilidades privadamente
- Usar variables de entorno para configuración sensible

---

## 🐛 Reporte de Bugs

### Crear un Issue

1. Ir a Issues en GitHub
2. Describir:
   - Qué esperabas que pasara
   - Qué pasó realmente
   - Pasos para reproducir
   - Ambiente (SO, versión Python, etc.)

### Ejemplo

```
## Descripción
La importación de archivos Excel falla con caracteres acentuados

## Pasos para reproducir
1. Crear archivo Excel con nombres en español
2. Importar vía endpoint `/api/routes/import_routes/`
3. Observar error de encoding

## Comportamiento esperado
Debería importar correctamente

## Ambiente
- OS: Windows 11
- Python: 3.10.5
- Django: 5.0.1
```

---

## 💡 Sugerencias de Features

Abrir un issue con:
- Descripción clara de la feature
- Por qué es útil
- Ejemplos de uso
- Posibles alternativas

---

## 📚 Recursos Útiles

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Git Workflow](https://git-scm.com/book/es/v2)

---

## 🎓 Decisiones Arquitectónicas

El proyecto sigue:
- **MVT Pattern**: Models-Views-Templates adaptado a API
- **Repository Pattern**: Para acceso a datos
- **Service Layer**: Lógica de negocio separada
- **Clean Architecture**: Dependencias hacia adentro

---

## 🚀 Merge Process

1. Al menos 1 review aprobado
2. Todos los tests pasando
3. Sin conflictos con main
4. Documentación actualizada
5. Merge con squash commit

---

## ❓ Preguntas?

- Abrir un Discussion en GitHub
- Contactar a los maintainers
- Revisar issues similares

---

¡Gracias por contribuir! 🙏
