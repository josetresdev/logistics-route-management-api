#!/usr/bin/env python
\"\"\"
Script para generar un archivo Excel de ejemplo para importación.

Uso:
    python generate_sample_excel.py [nombre_salida.xlsx]

Ejemplo:
    python generate_sample_excel.py example_routes.xlsx
\"\"\"

import sys
import pandas as pd
import json
from datetime import datetime, timedelta


def generate_sample_excel(output_file='sample_routes.xlsx'):
    \"\"\"Genera un archivo Excel de ejemplo para pruebas.\"\"\"

    # Datos de ejemplo para la hoja 'routes'
    routes_data = {
        'id_route': [1, 2, 3, 4, 5],
        'origin': [
            'Ciudad de Nueva York',
            'Los Ángeles',
            'Chicago',
            'Houston',
            'Phoenix'
        ],
        'destination': [
            'Boston',
            'San Francisco',
            'Dallas',
            'Nueva Orleans',
            'Los Ángeles'
        ],
        'distance_km': [
            215.5,
            559.0,
            920.0,
            676.5,
            599.0
        ],
        'priority': [1, 2, 1, 3, 2],
        'time_window_start': [
            datetime(2026, 3, 1, 8, 0, 0),
            datetime(2026, 3, 1, 9, 0, 0),
            datetime(2026, 3, 1, 10, 0, 0),
            datetime(2026, 3, 2, 8, 0, 0),
            datetime(2026, 3, 2, 9, 0, 0),
        ],
        'time_window_end': [
            datetime(2026, 3, 1, 18, 0, 0),
            datetime(2026, 3, 1, 19, 0, 0),
            datetime(2026, 3, 1, 20, 0, 0),
            datetime(2026, 3, 2, 18, 0, 0),
            datetime(2026, 3, 2, 19, 0, 0),
        ],
        'status': [
            'PENDING',
            'PENDING',
            'PENDING',
            'IN_PROGRESS',
            'PENDING'
        ],
    }

    # Datos de ejemplo para la hoja 'route_payload'
    payload_data = {
        'id_route': [1, 2, 3, 4, 5],
        'payload': [
            json.dumps({
                'notes': 'First express delivery',
                'vehicle_type': 'truck',
                'capacity_ton': 5.0
            }),
            json.dumps({
                'notes': 'Same-day delivery',
                'vehicle_type': 'van',\
                'capacity_ton': 2.0
            }),
            json.dumps({
                'notes': 'Standard delivery',
                'vehicle_type': 'truck',
                'capacity_ton': 10.0
            }),
            json.dumps({
                'notes': 'Priority handling - fragile items',
                'vehicle_type': 'van',
                'capacity_ton': 1.5
            }),
            json.dumps({
                'notes': 'Return shipment',
                'vehicle_type': 'truck',
                'capacity_ton': 8.0
            }),
        ],
    }

    # Crear DataFrames
    routes_df = pd.DataFrame(routes_data)
    payload_df = pd.DataFrame(payload_data)

    # Escribir a archivo Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        routes_df.to_excel(writer, sheet_name='routes', index=False)
        payload_df.to_excel(writer, sheet_name='route_payload', index=False)

    print(f\"✓ Archivo '{output_file}' creado exitosamente\")\
    print(f\"\\nDetalles:\")\
    print(f\"  - Hoja 'routes': {len(routes_df)} registros\")\
    print(f\"  - Hoja 'route_payload': {len(payload_df)} registros\")\
    print(f\"  - Tamaño: {pd.io.common.get_filepath_or_buffer(output_file)}\")


if __name__ == '__main__':\
    output_file = sys.argv[1] if len(sys.argv) > 1 else 'sample_routes.xlsx'\
    try:\
        generate_sample_excel(output_file)\
    except Exception as e:\
        print(f\"✗ Error: {e}\")\
        sys.exit(1)\
