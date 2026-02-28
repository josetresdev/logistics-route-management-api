from django.core.exceptions import ValidationError
from datetime import datetime


class RouteValidator:
    """
    Validador para reglas de negocio de rutas.
    """

    @staticmethod
    def validate_time_window(time_window_start, time_window_end):
        """
        Valida que la ventana de tiempo sea válida.
        
        Args:
            time_window_start (datetime): Inicio de ventana
            time_window_end (datetime): Fin de ventana
            
        Raises:
            ValidationError: Si las fechas no son válidas
        """
        if time_window_start >= time_window_end:
            raise ValidationError(
                "time_window_start must be before time_window_end"
            )

    @staticmethod
    def validate_distance(distance_km):
        """
        Valida que la distancia sea positiva.
        
        Args:
            distance_km (float): Distancia en kilómetros
            
        Raises:
            ValidationError: Si la distancia no es válida
        """
        if distance_km and distance_km <= 0:
            raise ValidationError("distance_km must be greater than 0")

    @staticmethod
    def validate_locations(origin, destination):
        """
        Valida que origen y destino sean diferentes.
        
        Args:
            origin (GeographicLocation): Ubicación de origen
            destination (GeographicLocation): Ubicación de destino
            
        Raises:
            ValidationError: Si origen y destino son iguales
        """
        if origin.id == destination.id:
            raise ValidationError(
                "Origin and destination must be different locations"
            )

    @staticmethod
    def validate_priority_level(priority_level):
        """
        Valida que el nivel de prioridad sea válido (1-4).
        
        Args:
            priority_level (int): Nivel de prioridad
            
        Raises:
            ValidationError: Si el nivel no es válido
        """
        valid_levels = [1, 2, 3, 4]
        if priority_level not in valid_levels:
            raise ValidationError(
                f"Priority level must be one of {valid_levels}"
            )


class ImportValidator:
    """
    Validador para archivos de importación.
    """

    REQUIRED_COLUMNS = [
        "origin",
        "destination",
        "priority",
        "status",
    ]

    OPTIONAL_COLUMNS = [
        "distance_km",
        "time_window_start",
        "time_window_end",
    ]

    @classmethod
    def validate_columns(cls, df):
        """
        Valida que el archivo Excel tenga las columnas requeridas.
        
        Args:
            df (DataFrame): DataFrame del archivo
            
        Raises:
            ValidationError: Si faltan columnas requeridas
        """
        missing_columns = [
            col for col in cls.REQUIRED_COLUMNS
            if col not in df.columns
        ]
        
        if missing_columns:
            raise ValidationError(
                f"Missing required columns: {', '.join(missing_columns)}"
            )

    @staticmethod
    def validate_row(row):
        """
        Valida una fila del archivo de importación.
        
        Args:
            row (dict): Fila del DataFrame
            
        Raises:
            ValidationError: Si la fila tiene datos inválidos
        """
        import pandas as pd
        
        # Validar campos requeridos
        for field in ["origin", "destination", "priority", "status"]:
            if field not in row or pd.isna(row[field]):
                raise ValidationError(f"Missing required field: {field}")
        
        # Validar que sean números
        try:
            int(row["origin"])
            int(row["destination"])
            int(row["priority"])
            int(row["status"])
        except (ValueError, TypeError):
            raise ValidationError(
                "origin, destination, priority, status must be integers"
            )
