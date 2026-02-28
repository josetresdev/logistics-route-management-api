from django.db import models


class RouteStatus(models.Model):
    """
    Catálogo de estados para rutas.
    Estados: PENDING (1), IN_PROGRESS (2), COMPLETED (3), FAILED (4)
    """
    code = models.CharField(max_length=30, unique=True, db_column="code")
    description = models.CharField(max_length=100, db_column="description")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "route_status"
        managed = False
        verbose_name = "Route Status"
        verbose_name_plural = "Route Statuses"

    def __str__(self):
        return f"{self.code} - {self.description}"


class PriorityCatalog(models.Model):
    """
    Catálogo de prioridades para rutas.
    Niveles: 1 (Baja), 2 (Normal), 3 (Alta), 4 (Crítica)
    """
    level = models.IntegerField(unique=True, db_column="level")
    description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="description"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "priority_catalog"
        managed = False
        verbose_name = "Priority Catalog"
        verbose_name_plural = "Priority Catalogs"

    def __str__(self):
        return f"Priority {self.level} - {self.description}"


class GeographicLocation(models.Model):
    """
    Ubicaciones geográficas para origen y destino de rutas.
    """
    name = models.CharField(max_length=150, db_column="name")
    address = models.TextField(db_column="address")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        db_column="latitude"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        db_column="longitude"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "geographic_locations"
        managed = False
        verbose_name = "Geographic Location"
        verbose_name_plural = "Geographic Locations"

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


class ImportBatch(models.Model):
    """
    Lote de importación para trackear origen de rutas importadas.
    """
    filename = models.CharField(max_length=255, db_column="filename")
    total_records = models.IntegerField(default=0, db_column="total_records")
    valid_records = models.IntegerField(default=0, db_column="valid_records")
    invalid_records = models.IntegerField(default=0, db_column="invalid_records")
    status = models.CharField(
        max_length=30,
        choices=[
            ("PENDING", "Pending"),
            ("PROCESSING", "Processing"),
            ("COMPLETED", "Completed"),
            ("FAILED", "Failed"),
        ],
        default="PENDING",
        db_column="status"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = "import_batches"
        managed = False
        verbose_name = "Import Batch"
        verbose_name_plural = "Import Batches"

    def __str__(self):
        return f"Batch {self.id} - {self.filename}"


class Route(models.Model):
    """
    Modelo principal de rutas logísticas.
    Mapea directamente a la tabla 'routes' en PostgreSQL.
    """
    origin = models.ForeignKey(
        GeographicLocation,
        on_delete=models.PROTECT,
        related_name="origin_routes",
        db_column="origin"
    )

    destination = models.ForeignKey(
        GeographicLocation,
        on_delete=models.PROTECT,
        related_name="destination_routes",
        db_column="destination"
    )

    distance_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        db_column="distance_km"
    )

    priority = models.ForeignKey(
        PriorityCatalog,
        on_delete=models.PROTECT,
        db_column="priority"
    )

    time_window_start = models.DateTimeField(db_column="time_window_start")
    time_window_end = models.DateTimeField(db_column="time_window_end")

    status = models.ForeignKey(
        RouteStatus,
        on_delete=models.PROTECT,
        db_column="status"
    )

    batch = models.ForeignKey(
        ImportBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="routes",
        db_column="batch_id"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = "routes"
        managed = False
        verbose_name = "Route"
        verbose_name_plural = "Routes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Route {self.id}: {self.origin} → {self.destination}"


class ExecutionLog(models.Model):
    """
    Auditoría de ejecuciones de rutas.
    Registra cada intento de ejecución con resultado y duración.
    """
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="execution_logs",
        db_column="route_id"
    )

    execution_time = models.DateTimeField(db_column="execution_time")
    
    result = models.CharField(
        max_length=30,
        choices=[
            ("SUCCESS", "Success"),
            ("FAILURE", "Failure"),
            ("PENDING", "Pending"),
        ],
        db_column="result"
    )

    message = models.TextField(db_column="message")
    
    execution_ms = models.IntegerField(
        null=True,
        blank=True,
        db_column="execution_ms"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "execution_logs"
        managed = False
        verbose_name = "Execution Log"
        verbose_name_plural = "Execution Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"ExecutionLog {self.id} - Route {self.route_id} - {self.result}"
