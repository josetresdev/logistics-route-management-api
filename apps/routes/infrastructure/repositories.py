from django.db.models import Q, Count
from apps.routes.domain.models import Route, ExecutionLog


class RouteRepository:
    """
    Repositorio para patrones de acceso a datos de Route.
    Encapsula queries complejas y mantiene la persistencia desacoplada.
    """

    @staticmethod
    def get_by_id(route_id):
        """Obtiene una ruta por ID con relaciones optimizadas."""
        return Route.objects.select_related(
            "origin",
            "destination",
            "priority",
            "status",
            "batch"
        ).get(id=route_id)

    @staticmethod
    def get_all_active():
        """Obtiene todas las rutas activas."""
        return Route.objects.filter(
            status__code__in=["PENDING", "IN_PROGRESS"]
        ).select_related("status", "priority", "origin", "destination")

    @staticmethod
    def get_by_status(status_code):
        """Filtra rutas por estado."""
        return Route.objects.filter(
            status__code=status_code
        ).select_related("origin", "destination", "status", "priority")

    @staticmethod
    def get_by_priority(priority_level):
        """Filtra rutas por prioridad."""
        return Route.objects.filter(
            priority__level=priority_level
        ).select_related("origin", "destination", "status", "priority")

    @staticmethod
    def get_by_location(location_id):
        """Obtiene rutas que usan una ubicación como origen o destino."""
        return Route.objects.filter(
            Q(origin_id=location_id) | Q(destination_id=location_id)
        ).select_related("origin", "destination", "status", "priority")

    @staticmethod
    def get_by_batch(batch_id):
        """Obtiene todas las rutas de un lote de importación."""
        return Route.objects.filter(
            batch_id=batch_id
        ).select_related("status", "priority", "origin", "destination")

    @staticmethod
    def get_statistics():
        """Obtiene estadísticas globales de rutas."""
        total = Route.objects.count()
        by_status = Route.objects.values(
            "status__code"
        ).annotate(count=Count("id"))
        by_priority = Route.objects.values(
            "priority__level"
        ).annotate(count=Count("id"))

        return {
            "total_routes": total,
            "by_status": list(by_status),
            "by_priority": list(by_priority),
        }

    @staticmethod
    def get_pending_routes():
        """Obtiene rutas pendientes de ejecución."""
        return Route.objects.filter(
            status__code="PENDING"
        ).select_related("origin", "destination", "priority")

    @staticmethod
    def get_failed_routes():
        """Obtiene rutas que fallaron."""
        return Route.objects.filter(
            status__code="FAILED"
        ).select_related("origin", "destination")


class ExecutionRepository:
    """
    Repositorio para patrones de acceso a datos de ExecutionLog.
    """

    @staticmethod
    def get_by_route(route_id):
        """Obtiene todas las ejecuciones de una ruta."""
        return ExecutionLog.objects.filter(
            route_id=route_id
        ).order_by("-created_at")

    @staticmethod
    def get_latest_by_route(route_id):
        """Obtiene la última ejecución de una ruta."""
        return ExecutionLog.objects.filter(
            route_id=route_id
        ).order_by("-created_at").first()

    @staticmethod
    def get_failed_executions():
        """Obtiene todas las ejecuciones fallidas."""
        return ExecutionLog.objects.filter(
            result="FAILURE"
        ).select_related("route")

    @staticmethod
    def get_execution_statistics(route_id):
        """Obtiene estadísticas de ejecución de una ruta."""
        logs = ExecutionLog.objects.filter(route_id=route_id)

        total = logs.count()
        successful = logs.filter(result="SUCCESS").count()
        failed = logs.filter(result="FAILURE").count()

        avg_execution_ms = logs.filter(
            execution_ms__isnull=False
        ).values_list("execution_ms", flat=True)
        avg_time = sum(avg_execution_ms) / len(avg_execution_ms) if avg_execution_ms else 0

        return {
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "avg_execution_ms": avg_time,
        }

    @staticmethod
    def get_by_date_range(start_date, end_date):
        """Obtiene ejecuciones en un rango de fechas."""
        return ExecutionLog.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).select_related("route")
