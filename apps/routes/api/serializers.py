from rest_framework import serializers
from apps.routes.domain.models import (
    Route,
    RouteStatus,
    ExecutionLog,
    ImportBatch,
)

# Nested serializers for relations

class LocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class RouteStatusSerializer(serializers.ModelSerializer):
    """Serializador para estados de ruta."""

    class Meta:
        model = RouteStatus
        fields = ["id", "code", "description"]
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
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)
    status = RouteStatusSerializer(read_only=True)

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
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)
    status = RouteStatusSerializer(read_only=True)
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
        ]
        read_only_fields = ["id", "created_at", "batch", "execution_logs"]

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

    origin_id = serializers.PrimaryKeyRelatedField(queryset=Route._meta.get_field('origin').related_model.objects.all(), source="origin")
    destination_id = serializers.PrimaryKeyRelatedField(queryset=Route._meta.get_field('destination').related_model.objects.all(), source="destination")

    class Meta:
        model = Route
        fields = [
            "origin_id",
            "destination_id",
            "distance_km",
            "priority",
            "status",
            "time_window_start",
            "time_window_end",
        ]


class RouteExecuteSerializer(serializers.Serializer):
    """Serializador para ejecutar rutas."""
    route_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        help_text="List of route IDs to execute"
    )


class ImportRouteFileSerializer(serializers.Serializer):
    """Serializador para importar archivo de rutas."""
    file = serializers.FileField(
        help_text="Excel file with routes data",
        required=True,
        allow_empty_file=False
    )
    batch_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="Optional batch name"
    )

    def validate_file(self, value):
        """Valida que el archivo sea Excel."""
        if not value:
            raise serializers.ValidationError(
                "El archivo no puede estar vacío. Asegúrate de que estés enviando el archivo de forma correcta."
            )

        if not hasattr(value, 'name') or not value.name:
            raise serializers.ValidationError(
                "El archivo debe incluir un nombre válido."
            )

        filename = value.name.lower()
        if not filename.endswith(('.xls', '.xlsx')):
            raise serializers.ValidationError(
                "El archivo debe ser Excel (.xls o .xlsx). Archivo recibido: " + filename
            )

        if hasattr(value, 'size'):
            if value.size == 0:
                raise serializers.ValidationError(
                    "El archivo está vacío. Por favor, envía un archivo con datos."
                )

            if value.size > 10 * 1024 * 1024:  # 10MB
                raise serializers.ValidationError(
                    f"El archivo excede el tamaño máximo de 10MB. Tamaño: {value.size / 1024 / 1024:.2f}MB"
                )

        return value


# Nested serializers for relations
class GeographicLocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
