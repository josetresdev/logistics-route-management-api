#!/usr/bin/env python
"""
Logistics Route Management API
Backend con Django y Django REST Framework
"""

__version__ = "1.0.0"
__author__ = "Development Team"
__description__ = """
Sistema de gestión completo de rutas logísticas que incluye:
- Importación desde Excel con validación
- Ejecución y auditoría de rutas
- API REST completa con filtros avanzados
- Autenticación y control de acceso
- Documentación OpenAPI/Swagger
- Deployment con Docker y Nginx
- Tests y validación de código
"""

PROJECT_STRUCTURE = {
    "config": "Configuración central de Django",
    "apps/routes/domain": "Modelos ORM y lógica de dominio",
    "apps/routes/application": "Servicios y validaciones",
    "apps/routes/infrastructure": "Repositorios y acceso a datos",
    "apps/routes/api": "Serializers, Views, URLs",
    "apps/routes/management": "Comandos personalizados",
    "apps/routes/tests": "Tests unitarios e integración",
}

FEATURES = [
    "✓ Arquitectura modular MVT con dominio limpio",
    "✓ Service layer para lógica de negocio",
    "✓ Repository pattern para persistencia",
    "✓ API REST completa con CRUD",
    "✓ Filtros avanzados y búsqueda",
    "✓ Importación desde Excel con validación",
    "✓ Ejecución y auditoría de rutas",
    "✓ Manejo global de errores",
    "✓ Autenticación y permisos",
    "✓ Paginación configurada",
    "✓ Testing automatizado",
    "✓ Docker y Docker Compose",
    "✓ Documentación Swagger OpenAPI",
    "✓ Nginx Reverse Proxy",
    "✓ PostgreSQL con schema customizado",
    "✓ Logging configurado",
    "✓ CORS habilitado",
]

PORTS = {
    "development": 8000,
    "production": 80,
    "postgresql": 5432,
    "nginx": 80,
}

MAIN_ENDPOINTS = {
    "API Base": "/api/",
    "Routes": "/api/routes/",
    "Route Statuses": "/api/route-statuses/",
    "Priorities": "/api/priorities/",
    "Locations": "/api/locations/",
    "Execution Logs": "/api/execution-logs/",
    "Import Batches": "/api/import-batches/",
    "Admin": "/admin/",
    "Docs Swagger": "/api/docs/",
    "Schema OpenAPI": "/api/schema/",
}
