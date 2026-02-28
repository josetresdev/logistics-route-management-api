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
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        from apps.routes.utils.response import ResponseHelper, PaginationMeta, SortMeta
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            pagination = PaginationMeta(
                current_page=int(request.query_params.get('page', 1)),
                per_page=self.paginator.page_size if hasattr(self, 'paginator') else len(page),
                total_items=self.paginator.page.paginator.count if hasattr(self, 'paginator') else len(queryset),
                total_pages=self.paginator.page.paginator.num_pages if hasattr(self, 'paginator') else 1,
            )
            sort = None
            ordering = request.query_params.get('ordering')
            if ordering:
                sort = SortMeta(sort_by=ordering.lstrip('-'), sort_order='DESC' if ordering.startswith('-') else 'ASC')
            return self.get_paginated_response(
                ResponseHelper.ok(serializer.data, message="Listado de rutas", pagination=pagination, sort=sort)
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            ResponseHelper.ok(serializer.data, message="Listado de rutas"),
            status=status.HTTP_200_OK
        )

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
            from apps.routes.utils.response import ResponseHelper
            return Response(
                ResponseHelper.ok(result, message="Rutas ejecutadas correctamente"),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            from apps.routes.utils.response import ResponseHelper
            return Response(
                ResponseHelper.error(str(e), code="EXECUTION_ERROR", status_code=status.HTTP_400_BAD_REQUEST),
                status=status.HTTP_400_BAD_REQUEST
            )

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
            from apps.routes.utils.response import ResponseHelper
            return Response(
                ResponseHelper.created(result, message="Importación completada"),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            from apps.routes.utils.response import ResponseHelper
            return Response(
                ResponseHelper.error(str(e), code="IMPORT_ERROR", status_code=status.HTTP_400_BAD_REQUEST),
                status=status.HTTP_400_BAD_REQUEST
            )

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

            from apps.routes.utils.response import ResponseHelper
            return Response(
                ResponseHelper.ok(history, message="Historial de ejecuciones obtenido"),
                status=status.HTTP_200_OK
            )
        except Route.DoesNotExist:
            from apps.routes.utils.response import ResponseHelper
            return Response(
                ResponseHelper.error("Route not found", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND),
                status=status.HTTP_404_NOT_FOUND
            )

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

        from apps.routes.utils.response import ResponseHelper
        return Response(
            ResponseHelper.ok(stats, message="Estadísticas obtenidas"),
            status=status.HTTP_200_OK
        )


class RouteStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para estados de rutas."""
    queryset = RouteStatus.objects.all()
    serializer_class = RouteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        from apps.routes.utils.response import ResponseHelper
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                ResponseHelper.ok(serializer.data, message="Listado de estados de ruta")
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            ResponseHelper.ok(serializer.data, message="Listado de estados de ruta"),
            status=status.HTTP_200_OK
        )


class PriorityCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para catálogo de prioridades."""
    queryset = PriorityCatalog.objects.all()
    serializer_class = PriorityCatalogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        from apps.routes.utils.response import ResponseHelper
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                ResponseHelper.ok(serializer.data, message="Listado de prioridades")
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            ResponseHelper.ok(serializer.data, message="Listado de prioridades"),
            status=status.HTTP_200_OK
        )


class GeographicLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para ubicaciones geográficas."""
    queryset = GeographicLocation.objects.all()
    serializer_class = GeographicLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["name", "address"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        from apps.routes.utils.response import ResponseHelper
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                ResponseHelper.ok(serializer.data, message="Listado de ubicaciones geográficas")
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            ResponseHelper.ok(serializer.data, message="Listado de ubicaciones geográficas"),
            status=status.HTTP_200_OK
        )


class ExecutionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para registros de ejecución."""
    queryset = ExecutionLog.objects.select_related("route").order_by("-created_at")
    serializer_class = ExecutionLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["route", "result"]
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        from apps.routes.utils.response import ResponseHelper
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                ResponseHelper.ok(serializer.data, message="Listado de ejecuciones")
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            ResponseHelper.ok(serializer.data, message="Listado de ejecuciones"),
            status=status.HTTP_200_OK
        )


class ImportBatchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de lectura para lotes de importación."""
    queryset = ImportBatch.objects.order_by("-created_at")
    serializer_class = ImportBatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status"]
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        from apps.routes.utils.response import ResponseHelper
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                ResponseHelper.ok(serializer.data, message="Listado de lotes de importación")
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            ResponseHelper.ok(serializer.data, message="Listado de lotes de importación"),
            status=status.HTTP_200_OK
        )
