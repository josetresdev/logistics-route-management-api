from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.routes.domain.models import (
    Route,
    RouteStatus,
    PriorityCatalog,
    GeographicLocation,
    ExecutionLog,
    ImportBatch,
)
from apps.routes.api.serializers import (
    RouteListSerializer,
    RouteDetailSerializer,
    RouteCreateSerializer,
    RouteExecuteSerializer,
    ImportRouteFileSerializer,
    ExecutionLogSerializer,
    RouteStatusSerializer,
    PriorityCatalogSerializer,
    GeographicLocationSerializer,
    ImportBatchSerializer,
)
from apps.routes.api.filters import RouteFilterSet
from apps.routes.application.services import (
    RouteService,
    ImportService,
    ExecutionService,
)
from apps.routes.infrastructure.repositories import (
    RouteRepository,
    ExecutionRepository,
)


class RouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar rutas.
    
    Operaciones disponibles:
    - GET /routes/ - Listar rutas
    - POST /routes/ - Crear ruta
    - GET /routes/{id}/ - Detalle de ruta
    - PUT /routes/{id}/ - Actualizar ruta
    - DELETE /routes/{id}/ - Eliminar ruta
    - POST /routes/{id}/execute/ - Ejecutar ruta
    - POST /routes/execute/ - Ejecutar múltiples rutas
    - POST /routes/import_routes/ - Importar desde Excel
    - GET /routes/{id}/execution_history/ - Historial de ejecuciones
    """
    
    queryset = Route.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = RouteFilterSet
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["origin__name", "destination__name"]
    ordering_fields = ["created_at", "priority", "status"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Retorna el serializador apropiado según la acción."""
        if self.action == "list":
            return RouteListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return RouteCreateSerializer
        elif self.action in ["execute", "execute_routes"]:
            return RouteExecuteSerializer
        elif self.action == "import_routes":
            return ImportRouteFileSerializer
        else:
            return RouteDetailSerializer

    def get_queryset(self):
        """Optimiza queries con select_related."""
        queryset = Route.objects.select_related(
            "origin",
            "destination",
            "priority",
            "status",
            "batch"
        )
        
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("execution_logs")
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Lista rutas con filtros y búsqueda.
        
        Query Parameters:
        - status: Código de estado (PENDING, IN_PROGRESS, COMPLETED, FAILED)
        - priority: Nivel de prioridad (1, 2, 3, 4)
        - origin: ID de ubicación origen
        - destination: ID de ubicación destino
        - created_after: Fecha mínima de creación
        - created_before: Fecha máxima de creación
        - search: Búsqueda en nombre de ubicación
        - ordering: Campo para ordenar (-created_at, priority, status)
        """
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def execute(self, request):
        """
        Ejecuta múltiples rutas.
        
        Request Body:
        {
            "route_ids": [1, 2, 3]
        }
        
        Response:
        {
            "data": {
                "total": 3,
                "executed": 3,
                "failed": 0,
                "executed_ids": [1, 2, 3],
                "errors": []
            },
            "errors": null,
            "status": 200
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        route_ids = serializer.validated_data.get("route_ids")
        
        try:
            result = RouteService.execute_routes(route_ids)
            return Response({
                "data": result,
                "errors": None,
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": None,
                "errors": {"detail": str(e)},
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="import_routes")
    def import_routes(self, request):
        """
        Importa rutas desde archivo Excel.
        
        Multipart Form Data:
        - file: Archivo Excel (.xls o .xlsx)
        - batch_name: (opcional) Nombre del lote
        
        Response:
        {
            "data": {
                "batch_id": 1,
                "filename": "routes.xlsx",
                "total": 100,
                "valid": 98,
                "invalid": 2,
                "errors": [...]
            },
            "errors": null,
            "status": 201
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data.get("file")
        batch_name = serializer.validated_data.get("batch_name")
        
        try:
            result = ImportService.import_file(file, batch_name)
            return Response({
                "data": result,
                "errors": None,
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "data": None,
                "errors": {"detail": str(e)},
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="execution_history")
    def execution_history(self, request, pk=None):
        """
        Obtiene historial de ejecuciones de una ruta.
        
        Response:
        {
            "data": [
                {
                    "id": 1,
                    "result": "SUCCESS",
                    "message": "Route executed successfully",
                    "execution_ms": 1234,
                    "execution_time": "2024-01-15T10:30:00Z",
                    "created_at": "2024-01-15T10:30:01Z"
                },
                ...
            ],
            "errors": null,
            "status": 200
        }
        """
        try:
            route = self.get_object()
            history = ExecutionService.get_execution_history(route.id)
            
            return Response({
                "data": history,
                "errors": None,
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Route.DoesNotExist:
            return Response({
                "data": None,
                "errors": {"detail": "Route not found"},
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """
        Obtiene estadísticas globales de rutas.
        
        Response:
        {
            "data": {
                "total_routes": 150,
                "by_status": [
                    {"status__code": "PENDING", "count": 50},
                    {"status__code": "COMPLETED", "count": 100}
                ],
                "by_priority": [
                    {"priority__level": 1, "count": 30},
                    {"priority__level": 2, "count": 120}
                ]
            },
            "errors": null,
            "status": 200
        }
        """
        stats = RouteRepository.get_statistics()
        
        return Response({
            "data": stats,
            "errors": None,
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


class RouteStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para estados de rutas."""
    queryset = RouteStatus.objects.all()
    serializer_class = RouteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class PriorityCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para catálogo de prioridades."""
    queryset = PriorityCatalog.objects.all()
    serializer_class = PriorityCatalogSerializer
    permission_classes = [permissions.IsAuthenticated]


class GeographicLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para ubicaciones geográficas."""
    queryset = GeographicLocation.objects.all()
    serializer_class = GeographicLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["name", "address"]


class ExecutionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para registros de ejecución."""
    queryset = ExecutionLog.objects.select_related("route").order_by("-created_at")
    serializer_class = ExecutionLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["route", "result"]
    filter_backends = [DjangoFilterBackend]


class ImportBatchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para lotes de importación."""
    queryset = ImportBatch.objects.order_by("-created_at")
    serializer_class = ImportBatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status"]
    filter_backends = [DjangoFilterBackend]
