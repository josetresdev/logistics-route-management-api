from django.db import models

# ============================================================
# GEOGRAPHIC LOCATION
# Tabla: routes_location
# ============================================================

class GeographicLocation(models.Model):
    name = models.CharField(max_length=255, db_column="name")
    address = models.TextField(db_column="address", null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, db_column="latitude", null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_column="longitude", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "routes_location"
        verbose_name = "Geographic Location"
        verbose_name_plural = "Geographic Locations"

    def __str__(self):
        return self.name
from django.db import models


# ============================================================
# ROUTE STATUS
# Tabla: routes_status
# ============================================================

class RouteStatus(models.Model):
    code = models.CharField(max_length=30, unique=True, db_column="code")
    description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="description"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "routes_status"
        verbose_name = "Route Status"
        verbose_name_plural = "Route Statuses"

    def __str__(self):
        return self.code


# ============================================================
# IMPORT BATCH
# Tabla: routes_import_batch
# ============================================================

class ImportBatch(models.Model):
    filename = models.CharField(max_length=255, db_column="filename")
    total_records = models.IntegerField(
        default=0,
        db_column="total_records"
    )
    valid_records = models.IntegerField(
        default=0,
        db_column="valid_records"
    )
    invalid_records = models.IntegerField(
        default=0,
        db_column="invalid_records"
    )
    status = models.CharField(
        max_length=30,
        default="PENDING",
        db_column="status"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column="created_at"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_column="updated_at"
    )

    class Meta:
        db_table = "routes_import_batch"
        verbose_name = "Import Batch"
        verbose_name_plural = "Import Batches"

    def __str__(self):
        return f"Batch {self.id} - {self.filename}"


# ============================================================
# ROUTES
# Tabla: routes_route
# ============================================================

class Route(models.Model):

    origin = models.ForeignKey(
        GeographicLocation,
        on_delete=models.PROTECT,
        related_name="routes_origin",
        db_column="origin_id"
    )
    destination = models.ForeignKey(
        GeographicLocation,
        on_delete=models.PROTECT,
        related_name="routes_destination",
        db_column="destination_id"
    )

    distance_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="distance_km"
    )

    priority = models.IntegerField(db_column="priority")

    time_window_start = models.DateTimeField(
        db_column="time_window_start"
    )
    time_window_end = models.DateTimeField(
        db_column="time_window_end"
    )

    status = models.ForeignKey(
        RouteStatus,
        on_delete=models.SET_NULL,
        null=True,
        db_column="status_id"
    )

    batch = models.ForeignKey(
        ImportBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="routes",
        db_column="batch_id"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column="created_at"
    )

    class Meta:
        ordering = ["-created_at"]
        db_table = "routes_route"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "origin_id",
                    "destination_id",
                    "time_window_start",
                    "time_window_end",
                ],
                name="unique_route_combination",
            )
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.origin.name} → {self.destination.name}" if self.origin and self.destination else "Route"


# ============================================================
# ROUTE PAYLOAD
# Tabla: routes_payload
# ============================================================

class RoutePayload(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        db_column="route_id",
        related_name="payloads"
    )

    payload = models.JSONField(db_column="payload")

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column="created_at"
    )

    class Meta:
        db_table = "routes_payload"

    def __str__(self):
        return f"Payload for Route {self.route_id}"


# ============================================================
# EXECUTION LOGS
# Tabla: routes_execution_log
# ============================================================

class ExecutionLog(models.Model):

    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="execution_logs",
        db_column="route_id"
    )

    execution_time = models.DateTimeField(
        db_column="execution_time"
    )

    result = models.CharField(
        max_length=30,
        db_column="result"
    )

    message = models.TextField(
        null=True,
        blank=True,
        db_column="message"
    )

    execution_ms = models.IntegerField(
        null=True,
        blank=True,
        db_column="execution_ms"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column="created_at"
    )

    class Meta:
        ordering = ["-created_at"]
        db_table = "routes_execution_log"

    def __str__(self):
        return f"Execution {self.id} - Route {self.route_id}"
