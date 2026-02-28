from django.db import models


class RouteQuerySet(models.QuerySet):
    """
    Custom QuerySet para Route con optimizaciones comunes.
    """
    
    def active(self):
        """Retorna solo rutas activas (no completadas, no fallidas)."""
        return self.exclude(status__code__in=["COMPLETED", "FAILED"])
    
    def with_locations(self):
        """Prefetch relacionados para optimización n+1."""
        return self.select_related(
            "origin",
            "destination",
            "priority",
            "status",
            "batch"
        )
    
    def by_priority(self, level):
        """Filtra rutas por nivel de prioridad."""
        return self.filter(priority__level=level)
    
    def by_status(self, status_code):
        """Filtra rutas por código de estado."""
        return self.filter(status__code=status_code)


class RouteManager(models.Manager):
    """
    Manager personalizado para Route.
    """
    
    def get_queryset(self):
        return RouteQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def with_locations(self):
        return self.get_queryset().with_locations()
    
    def by_priority(self, level):
        return self.get_queryset().by_priority(level)
    
    def by_status(self, status_code):
        return self.get_queryset().by_status(status_code)
