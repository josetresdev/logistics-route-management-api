from django.db import transaction
from django.utils import timezone
from datetime import datetime
import pandas as pd
from io import BytesIO

from apps.routes.domain.models import (
    Route,
    ExecutionLog,
    ImportBatch,
    RouteStatus,
)
from apps.routes.exceptions import (
    InvalidRouteData,
    ImportError,
    ExecutionError,
)


class RouteService:
    """
    Servicio de aplicación para gestionar rutas.
    Encapsula lógica de negocio y transacciones.
    """

    @staticmethod
    @transaction.atomic
    def create_route(validated_data):
        """
        Crea una nueva ruta con validaciones y auditoría.
        
        Args:
            validated_data (dict): Datos validados de la ruta
            
        Returns:
            Route: Instancia de ruta creada
            
        Raises:
            InvalidRouteData: Si los datos no son válidos
        """
        try:
            route = Route.objects.create(**validated_data)
            return route
        except Exception as e:
            raise InvalidRouteData(f"Error creating route: {str(e)}")

    @staticmethod
    @transaction.atomic
    def execute_routes(route_ids):
        """
        Ejecuta múltiples rutas y registra auditoría.
        
        Args:
            route_ids (list): Lista de IDs de rutas a ejecutar
            
        Returns:
            dict: Resumen de ejecución con resultados
            
        Raises:
            ExecutionError: Si hay error en la ejecución
        """
        try:
            routes = Route.objects.filter(
                id__in=route_ids
            ).select_related("status")
            
            if not routes.exists():
                raise ExecutionError("No routes found with provided IDs")
            
            executed = []
            errors = []
            
            # Obtener estado "IN_PROGRESS"
            try:
                in_progress_status = RouteStatus.objects.get(code="IN_PROGRESS")
            except RouteStatus.DoesNotExist:
                raise ExecutionError("IN_PROGRESS status not found in database")
            
            start_time = timezone.now()
            
            for route in routes:
                try:
                    # Actualizar estado
                    route.status = in_progress_status
                    route.save(update_fields=["status", "updated_at"])
                    
                    # Simular procesamiento
                    execution_time = (timezone.now() - start_time).total_seconds() * 1000
                    
                    # Registrar en auditoría
                    ExecutionLog.objects.create(
                        route=route,
                        execution_time=timezone.now(),
                        result="SUCCESS",
                        message="Route executed successfully",
                        execution_ms=int(execution_time)
                    )
                    
                    executed.append(route.id)
                    
                except Exception as e:
                    errors.append({
                        "route_id": route.id,
                        "error": str(e)
                    })
            
            return {
                "total": len(routes),
                "executed": len(executed),
                "failed": len(errors),
                "executed_ids": executed,
                "errors": errors
            }
            
        except ExecutionError:
            raise
        except Exception as e:
            raise ExecutionError(f"Error executing routes: {str(e)}")

    @staticmethod
    def get_route_status(route_id):
        """
        Obtiene el estado actual de una ruta.
        
        Args:
            route_id (int): ID de la ruta
            
        Returns:
            dict: Estado y detalles de la ruta
        """
        try:
            route = Route.objects.select_related(
                "status",
                "priority",
                "origin",
                "destination"
            ).get(id=route_id)
            
            latest_execution = route.execution_logs.order_by(
                "-created_at"
            ).first()
            
            return {
                "id": route.id,
                "origin": str(route.origin),
                "destination": str(route.destination),
                "priority": route.priority.level,
                "status": route.status.code,
                "last_execution": latest_execution.created_at if latest_execution else None,
                "last_execution_result": latest_execution.result if latest_execution else None,
            }
        except Route.DoesNotExist:
            raise InvalidRouteData(f"Route {route_id} not found")


class ImportService:
    """
    Servicio para importar rutas desde archivos Excel.
    """

    @staticmethod
    @transaction.atomic
    def import_file(file, batch_name=None):
        """
        Importa rutas desde archivo Excel.
        
        Args:
            file: Archivo Excel (InMemoryUploadedFile)
            batch_name (str): Nombre del lote de importación
            
        Returns:
            dict: Resumen de importación
            
        Raises:
            ImportError: Si hay error en la importación
        """
        try:
            # Crear registro de lote
            batch = ImportBatch.objects.create(
                filename=file.name if hasattr(file, 'name') else batch_name or "unknown",
                status="PROCESSING"
            )
            
            # Leer archivo Excel
            df = pd.read_excel(file)
            
            errors = []
            valid_records = []
            
            for index, row in df.iterrows():
                try:
                    # Convertir fila a diccionario
                    data = row.to_dict()
                    
                    # Validaciones básicas
                    required_fields = ["origin", "destination", "priority", "status"]
                    missing_fields = [
                        field for field in required_fields
                        if field not in data or pd.isna(data[field])
                    ]
                    
                    if missing_fields:
                        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
                    
                    # Preparar datos para crear ruta
                    route_data = {
                        "batch": batch,
                        "origin_id": int(data["origin"]),
                        "destination_id": int(data["destination"]),
                        "priority_id": int(data["priority"]),
                        "status_id": int(data["status"]),
                        "distance_km": float(data.get("distance_km", 0)),
                        "time_window_start": data.get("time_window_start"),
                        "time_window_end": data.get("time_window_end"),
                    }
                    
                    valid_records.append(Route(**route_data))
                    
                except Exception as e:
                    errors.append({
                        "row": index + 2,  # +2 porque fila 1 es header
                        "error": str(e),
                        "values": row.to_dict()
                    })
            
            # Crear rutas en lote
            created_routes = Route.objects.bulk_create(valid_records)
            
            # Actualizar lote
            batch.total_records = len(df)
            batch.valid_records = len(created_routes)
            batch.invalid_records = len(errors)
            batch.status = "COMPLETED" if not errors else "COMPLETED"
            batch.save()
            
            return {
                "batch_id": batch.id,
                "filename": batch.filename,
                "total": len(df),
                "valid": len(created_routes),
                "invalid": len(errors),
                "errors": errors,
                "message": f"Import completed: {len(created_routes)} valid routes imported"
            }
            
        except Exception as e:
            if 'batch' in locals():
                batch.status = "FAILED"
                batch.save()
            raise ImportError(f"Error importing file: {str(e)}")

    @staticmethod
    def get_import_history(limit=10):
        """
        Obtiene histórico de importaciones.
        
        Args:
            limit (int): Número máximo de registros
            
        Returns:
            list: Lista de lotes de importación
        """
        batches = ImportBatch.objects.order_by("-created_at")[:limit]
        
        return [
            {
                "id": batch.id,
                "filename": batch.filename,
                "total_records": batch.total_records,
                "valid_records": batch.valid_records,
                "invalid_records": batch.invalid_records,
                "status": batch.status,
                "created_at": batch.created_at.isoformat(),
            }
            for batch in batches
        ]


class ExecutionService:
    """
    Servicio para gestionar auditoría de ejecuciones.
    """

    @staticmethod
    @transaction.atomic
    def log_execution(route_id, result, message, execution_ms=None):
        """
        Registra una ejecución de ruta.
        
        Args:
            route_id (int): ID de la ruta
            result (str): Resultado (SUCCESS, FAILURE, PENDING)
            message (str): Mensaje descriptivo
            execution_ms (int): Duración en milisegundos
            
        Returns:
            ExecutionLog: Registro de ejecución creado
        """
        try:
            route = Route.objects.get(id=route_id)
            
            execution_log = ExecutionLog.objects.create(
                route=route,
                execution_time=timezone.now(),
                result=result,
                message=message,
                execution_ms=execution_ms
            )
            
            return execution_log
            
        except Route.DoesNotExist:
            raise InvalidRouteData(f"Route {route_id} not found")

    @staticmethod
    def get_execution_history(route_id, limit=50):
        """
        Obtiene histórico de ejecuciones de una ruta.
        
        Args:
            route_id (int): ID de la ruta
            limit (int): Número máximo de registros
            
        Returns:
            list: Historial de ejecuciones
        """
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
