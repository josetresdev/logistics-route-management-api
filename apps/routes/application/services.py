from django.db import transaction
from django.utils import timezone
from django.db.utils import IntegrityError
import pandas as pd
import json

from apps.routes.domain.models import (
    Route,
    ExecutionLog,
    ImportBatch,
    RouteStatus,
    RoutePayload,
    GeographicLocation,
)
from apps.routes.exceptions import (
    InvalidRouteData,
    ImportError,
    ExecutionError,
)


# ============================================================
# ROUTE SERVICE (SIN CAMBIOS DE CONTRATO)
# ============================================================

class RouteService:

    @staticmethod
    @transaction.atomic
    def create_route(validated_data):
        RouteService._validate_business_rules(validated_data)
        try:
            return Route.objects.create(**validated_data)
        except IntegrityError as e:
            raise InvalidRouteData(f"Database constraint error: {str(e)}")
        except Exception as e:
            raise InvalidRouteData(str(e))

    @staticmethod
    def _validate_business_rules(data):
        required = [
            "origin",
            "destination",
            "distance_km",
            "priority",
            "time_window_start",
            "time_window_end",
            "status",
        ]

        for field in required:
            if data.get(field) in [None, "", "nan"]:
                raise InvalidRouteData(f"{field} is required")

        if float(data["distance_km"]) <= 0:
            raise InvalidRouteData("distance_km must be greater than 0")

        if int(data["priority"]) <= 0:
            raise InvalidRouteData("priority must be positive integer")

        if data["time_window_start"] >= data["time_window_end"]:
            raise InvalidRouteData("Invalid time window")

        duplicate = Route.objects.filter(
            origin_id=getattr(data["origin"], "id", data["origin"]),
            destination_id=getattr(data["destination"], "id", data["destination"]),
            time_window_start=data["time_window_start"],
            time_window_end=data["time_window_end"],
        ).exists()

        if duplicate:
            raise InvalidRouteData("Duplicate route detected")

    @staticmethod
    @transaction.atomic
    def execute_routes(route_ids):

        routes = Route.objects.filter(id__in=route_ids)

        if not routes.exists():
            raise ExecutionError("No routes found")

        status_obj, _ = RouteStatus.objects.get_or_create(code="IN_PROGRESS")

        executed = []
        errors = []

        for route in routes:
            try:
                start = timezone.now()

                route.status = status_obj
                route.save(update_fields=["status"])

                execution_ms = int(
                    (timezone.now() - start).total_seconds() * 1000
                )

                ExecutionLog.objects.create(
                    route=route,
                    execution_time=timezone.now(),
                    result="SUCCESS",
                    message="Route executed successfully",
                    execution_ms=execution_ms,
                )

                executed.append(route.id)

            except Exception as e:
                errors.append({
                    "route_id": route.id,
                    "error": str(e),
                })

        return {
            "total": routes.count(),
            "executed": len(executed),
            "failed": len(errors),
            "executed_ids": executed,
            "errors": errors,
        }


# ============================================================
# IMPORT SERVICE (AJUSTADO A FK REAL SIN CAMBIAR TU FLUJO)
# ============================================================

class ImportService:

    @staticmethod
    def _normalize_columns(df):
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df

    @staticmethod
    def _clean(value):
        if pd.isna(value):
            return None
        return str(value).strip()

    @staticmethod
    def _get_or_create_batch_locations(location_names):
        """Bulk get_or_create for all locations at once"""
        location_names = set(filter(None, location_names))

        # Get existing locations
        existing = {
            loc.name: loc
            for loc in GeographicLocation.objects.filter(name__in=location_names)
        }

        # Find missing ones
        missing_names = location_names - set(existing.keys())

        # Bulk create missing locations
        if missing_names:
            new_locs = [
                GeographicLocation(name=name)
                for name in missing_names
            ]
            created = GeographicLocation.objects.bulk_create(new_locs, batch_size=1000)
            for loc in created:
                existing[loc.name] = loc

        return existing

    @staticmethod
    def import_file(file, batch_name=None):

        if not file:
            raise ImportError("No file provided")

        if not hasattr(file, 'read'):
            raise ImportError("Invalid file object: must have a read() method")

        if not hasattr(file, 'name'):
            raise ImportError("Invalid file object: must have a name attribute")

        filename = file.name

        if not filename.lower().endswith(('.xls', '.xlsx')):
            raise ImportError(
                f"Invalid file type. Expected .xls or .xlsx, got: {filename}"
            )

        batch = ImportBatch.objects.create(
            filename=batch_name or filename,
            status="PROCESSING",
        )

        try:

            if hasattr(file, 'seek'):
                file.seek(0)

            routes_df = pd.read_excel(file, sheet_name="routes")

            if hasattr(file, 'seek'):
                file.seek(0)

            payload_df = pd.read_excel(file, sheet_name="route_payload")

            routes_df = ImportService._normalize_columns(routes_df)
            payload_df = ImportService._normalize_columns(payload_df)

            id_cols = ["idroute", "id_route"]

            route_id_col = next(
                (c for c in id_cols if c in routes_df.columns),
                None
            )

            payload_id_col = next(
                (c for c in id_cols if c in payload_df.columns),
                None
            )

            if not route_id_col or not payload_id_col:
                raise ImportError("ID column not found in Excel sheets")

            df = routes_df.merge(
                payload_df,
                how="left",
                left_on=route_id_col,
                right_on=payload_id_col,
            )

            status_map = {
                s.code: s for s in RouteStatus.objects.all()
            }

            # Bulk get_or_create all locations first
            all_location_names = set(
                filter(None, list(df.get("origin")) + list(df.get("destination")))
            )
            location_map = ImportService._get_or_create_batch_locations(all_location_names)

            errors = []
            valid_routes = []
            payload_objects = []

            for index, row in df.iterrows():
                try:
                    origin_name = ImportService._clean(row.get("origin"))
                    destination_name = ImportService._clean(row.get("destination"))

                    if not origin_name or not destination_name:
                        raise ValueError("Origin and destination required")

                    # Use pre-loaded location map (no queries)
                    origin = location_map.get(origin_name)
                    destination = location_map.get(destination_name)

                    if not origin or not destination:
                        raise ValueError("Location not found in map")

                    distance = float(row.get("distance_km") or 0)
                    if distance <= 0:
                        raise ValueError("Distance must be greater than 0")

                    priority = int(row.get("priority") or 0)
                    if priority <= 0:
                        raise ValueError("Priority must be positive integer")

                    start = pd.to_datetime(row.get("time_window_start"))
                    end = pd.to_datetime(row.get("time_window_end"))

                    if pd.isna(start) or pd.isna(end) or start >= end:
                        raise ValueError("Invalid time window")

                    status_code = ImportService._clean(row.get("status"))

                    if not status_code:
                        raise ValueError("Status required")

                    if status_code not in status_map:
                        status_obj = RouteStatus.objects.create(
                            code=status_code,
                            description=status_code
                        )
                        status_map[status_code] = status_obj

                    route = Route(
                        origin=origin,
                        destination=destination,
                        distance_km=distance,
                        priority=priority,
                        time_window_start=start,
                        time_window_end=end,
                        status=status_map[status_code],
                        batch=batch,
                    )

                    valid_routes.append(route)

                except Exception as e:
                    errors.append({
                        "row": index + 2,
                        "error": str(e),
                        "data": row.to_dict(),
                    })

            if valid_routes:

                created_routes = Route.objects.bulk_create(
                    valid_routes,
                    batch_size=1000
                )

                for route_obj, (_, row) in zip(created_routes, df.iterrows()):
                    payload_data = row.get("payload")

                    if payload_data:
                        try:
                            payload_objects.append(
                                RoutePayload(
                                    route=route_obj,
                                    payload=json.loads(payload_data)
                                )
                            )
                        except json.JSONDecodeError:
                            errors.append({
                                "route_id": route_obj.id,
                                "error": "Invalid JSON payload",
                            })

                if payload_objects:
                    RoutePayload.objects.bulk_create(
                        payload_objects,
                        batch_size=1000
                    )

            batch.total_records = len(df)
            batch.valid_records = len(valid_routes)
            batch.invalid_records = len(errors)
            batch.status = "FAILED" if not valid_routes else "COMPLETED"
            batch.updated_at = timezone.now()
            batch.save()

            return {
                "batch_id": batch.id,
                "total": len(df),
                "valid": len(valid_routes),
                "invalid": len(errors),
                "errors": errors,
            }

        except FileNotFoundError as e:
            batch.status = "FAILED"
            batch.save()
            raise ImportError(
                f"File not found or cannot be read: {str(e)}"
            )

        except Exception as e:
            batch.status = "FAILED"
            batch.save()

            error_msg = str(e)

            if "sheet_name" in error_msg:
                raise ImportError(
                    "Excel file must contain sheets named "
                    "'routes' and 'route_payload'."
                )

            elif "openpyxl" in error_msg or "xlrd" in error_msg:
                raise ImportError(
                    "Excel library not installed. "
                    "Install openpyxl or xlrd."
                )

            else:
                raise ImportError(f"Error reading file: {error_msg}")


# ============================================================
# EXECUTION SERVICE (SIN CAMBIOS)
# ============================================================

class ExecutionService:

    @staticmethod
    @transaction.atomic
    def log_execution(route_id, result, message, execution_ms=None):

        try:
            route = Route.objects.get(id=route_id)
        except Route.DoesNotExist:
            raise InvalidRouteData("Route not found")

        return ExecutionLog.objects.create(
            route=route,
            execution_time=timezone.now(),
            result=result,
            message=message,
            execution_ms=execution_ms,
        )

    @staticmethod
    def get_execution_history(route_id, limit=50):

        logs = ExecutionLog.objects.filter(
            route_id=route_id
        ).order_by("-created_at")[:limit]

        return [
            {
                "id": log.id,
                "result": log.result,
                "message": log.message,
                "execution_ms": log.execution_ms,
                "execution_time": log.execution_time.isoformat(),
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ]
