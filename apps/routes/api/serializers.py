from rest_framework import serializers
from apps.routes.domain.models import (
    Route,
    RouteStatus,
    PriorityCatalog,
    GeographicLocation,
    ExecutionLog,
    ImportBatch,
)


class GeographicLocationSerializer(serializers.ModelSerializer):
    """Serializador para ubicaciones geográficas."""
    
    class Meta:
        model = GeographicLocation
        fields = ["id", "name", "address", "latitude", "longitude"]
        read_only_fields = ["id"]


class RouteStatusSerializer(serializers.ModelSerializer):
    """Serializador para estados de ruta."""
    
    class Meta:
        model = RouteStatus
        fields = ["id", "code", "description"]
        read_only_fields = ["id"]


class PriorityCatalogSerializer(serializers.ModelSerializer):
    """Serializador para catálogo de prioridades."""
    
    class Meta:
        model = PriorityCatalog
        fields = ["id", "level", "description"]
        read_only_fields = ["id"]


class ImportBatchSerializer(serializers.ModelSerializer):
    """Serializador para lotes de importación."""
    
    class Meta:
        model = ImportBatch
        fields = [
            "id",
            "filename",
            "total_records",
            "valid_records",
            "invalid_records",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ExecutionLogSerializer(serializers.ModelSerializer):
    """Serializador para registros de ejecución."""
    
    class Meta:
        model = ExecutionLog
        fields = [
            "id",
            "route",
            "execution_time",
            "result",
            "message",
            "execution_ms",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class RouteListSerializer(serializers.ModelSerializer):
    """
    Serializador de lista para rutas (lightweight).
    Usa nested serializers para relaciones.
    """
    origin = GeographicLocationSerializer(read_only=True)
    destination = GeographicLocationSerializer(read_only=True)
    status = RouteStatusSerializer(read_only=True)
    priority = PriorityCatalogSerializer(read_only=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "origin",
            "destination",
            "distance_km",
            "priority",
            "status",
            "time_window_start",
            "time_window_end",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class RouteDetailSerializer(serializers.ModelSerializer):
    """
    Serializador detallado para rutas.
    Incluye toda la información y relaciones.
    """
    origin = GeographicLocationSerializer(read_only=True)
    destination = GeographicLocationSerializer(read_only=True)
    status = RouteStatusSerializer(read_only=True)
    priority = PriorityCatalogSerializer(read_only=True)
    batch = ImportBatchSerializer(read_only=True)
    execution_logs = ExecutionLogSerializer(many=True, read_only=True)

    # IDs para escritura
    origin_id = serializers.IntegerField(write_only=True)
    destination_id = serializers.IntegerField(write_only=True)
    status_id = serializers.IntegerField(write_only=True)
    priority_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "origin",
            "destination",
            "origin_id",
            "destination_id",
            "distance_km",
            "priority",
            "priority_id",
            "status",
            "status_id",
            "time_window_start",
            "time_window_end",
            "batch",
            "execution_logs",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "batch", "execution_logs"]

    def validate(self, data):
        """Validaciones a nivel de objeto."""
        # Verificar que origen y destino sean diferentes
        if data.get("origin_id") == data.get("destination_id"):
            raise serializers.ValidationError(
                "Origin and destination must be different locations"
            )
        
        # Validar ventana de tiempo si está presente
        start = data.get("time_window_start")
        end = data.get("time_window_end")
        
        if start and end:
            if start >= end:
                raise serializers.ValidationError(
                    "time_window_start must be before time_window_end"
                )
        
        return data


class RouteCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear rutas."""
    
    class Meta:
        model = Route
        fields = [
            "origin",
            "destination",
            "distance_km",
            "priority",
            "status",
            "time_window_start",
            "time_window_end",
        ]

    def create(self, validated_data):
        """Crea una ruta con validaciones."""
        route = Route.objects.create(**validated_data)
        return route


class RouteExecuteSerializer(serializers.Serializer):
    """Serializador para ejecutar rutas."""
    route_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        help_text="List of route IDs to execute"
    )


class ImportRouteFileSerializer(serializers.Serializer):
    """Serializador para importar archivo de rutas."""
    file = serializers.FileField(help_text="Excel file with routes data")
    batch_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="Optional batch name"
    )

    def validate_file(self, value):
        """Valida que el archivo sea Excel."""
        if not value.name.endswith(('.xls', '.xlsx')):
            raise serializers.ValidationError(
                "File must be an Excel file (.xls or .xlsx)"
            )
        
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError(
                "File size must not exceed 10MB"
            )
        
        return value
