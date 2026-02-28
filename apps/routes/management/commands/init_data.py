from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.routes.domain.models import (
    RouteStatus,
    PriorityCatalog,
    GeographicLocation,
)


class Command(BaseCommand):
    """
    Comando para cargar datos iniciales en la base de datos.
    Uso: python manage.py init_data
    """
    
    help = "Initialize database with default data (statuses, priorities, locations)"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Initializing database with default data...")
        
        # Crear estados de rutas
        self.create_route_statuses()
        
        # Crear catálogo de prioridades
        self.create_priorities()
        
        # Crear ubicaciones geográficas de ejemplo
        self.create_sample_locations()
        
        self.stdout.write(
            self.style.SUCCESS("✅ Database initialized successfully!")
        )

    def create_route_statuses(self):
        """Crear estados de rutas."""
        statuses = [
            {"code": "PENDING", "description": "Pending execution"},
            {"code": "IN_PROGRESS", "description": "Route in progress"},
            {"code": "COMPLETED", "description": "Route completed successfully"},
            {"code": "FAILED", "description": "Route execution failed"},
        ]
        
        for status_data in statuses:
            status, created = RouteStatus.objects.get_or_create(
                code=status_data["code"],
                defaults={
                    "description": status_data["description"],
                    "created_at": timezone.now(),
                }
            )
            
            if created:
                self.stdout.write(
                    f"  ✓ Created route status: {status.code}"
                )
            else:
                self.stdout.write(
                    f"  - Route status already exists: {status.code}"
                )

    def create_priorities(self):
        """Crear catálogo de prioridades."""
        priorities = [
            {"level": 1, "description": "Low priority"},
            {"level": 2, "description": "Normal priority"},
            {"level": 3, "description": "High priority"},
            {"level": 4, "description": "Critical priority"},
        ]
        
        for priority_data in priorities:
            priority, created = PriorityCatalog.objects.get_or_create(
                level=priority_data["level"],
                defaults={
                    "description": priority_data["description"],
                    "created_at": timezone.now(),
                }
            )
            
            if created:
                self.stdout.write(
                    f"  ✓ Created priority: Level {priority.level}"
                )
            else:
                self.stdout.write(
                    f"  - Priority already exists: Level {priority.level}"
                )

    def create_sample_locations(self):
        """Crear ubicaciones geográficas de ejemplo."""
        locations = [
            {
                "name": "Santiago Centro",
                "address": "Plaza de Armas, Santiago",
                "latitude": "-33.4372",
                "longitude": "-70.6659",
            },
            {
                "name": "Valparaíso Puerto",
                "address": "Cerro Alegre, Valparaíso",
                "latitude": "-33.0472",
                "longitude": "-71.6127",
            },
            {
                "name": "Viña del Mar",
                "address": "Avenida Perú, Viña del Mar",
                "latitude": "-33.0254",
                "longitude": "-71.5520",
            },
            {
                "name": "Concepción Centro",
                "address": "Calle Colo Colo, Concepción",
                "latitude": "-36.8267",
                "longitude": "-73.0372",
            },
            {
                "name": "Temuco Centro",
                "address": "Avenida Arturo Prat, Temuco",
                "latitude": "-38.7372",
                "longitude": "-72.5909",
            },
        ]
        
        for location_data in locations:
            location, created = GeographicLocation.objects.get_or_create(
                name=location_data["name"],
                defaults={
                    "address": location_data["address"],
                    "latitude": location_data["latitude"],
                    "longitude": location_data["longitude"],
                    "created_at": timezone.now(),
                }
            )
            
            if created:
                self.stdout.write(
                    f"  ✓ Created location: {location.name}"
                )
            else:
                self.stdout.write(
                    f"  - Location already exists: {location.name}"
                )
