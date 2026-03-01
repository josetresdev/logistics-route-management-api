#!/usr/bin/env python
"""
Script de prueba rápida para el endpoint de importación.

Uso:
    python test_import_endpoint.py <token> <url_base>

Ejemplo:
    python test_import_endpoint.py 8b57ab78b769b0bb358c60b2eef025c6efc895a2 http://localhost:8000
"""

import sys
import json
import requests
import pandas as pd
import io
from pathlib import Path


def create_test_excel():
    \"\"\"Crea un archivo Excel de prueba.\"\"\"
    routes_data = {
        'id_route': [1, 2, 3],
        'origin': ['Nueva York', 'Los Ángeles', 'Chicago'],
        'destination': ['Boston', 'San Francisco', 'Dallas'],
        'distance_km': [215.5, 559.0, 920.0],
        'priority': [1, 2, 1],
        'time_window_start': [
            '2026-03-01 08:00:00',
            '2026-03-01 09:00:00',
            '2026-03-01 10:00:00',
        ],
        'time_window_end': [
            '2026-03-01 18:00:00',
            '2026-03-01 19:00:00',
            '2026-03-01 20:00:00',
        ],
        'status': ['PENDING', 'PENDING', 'PENDING'],
    }

    payload_data = {
        'id_route': [1, 2, 3],
        'payload': [
            json.dumps({'notes': 'Route 1'}),
            json.dumps({'notes': 'Route 2'}),
            json.dumps({'notes': 'Route 3'}),
        ],
    }

    routes_df = pd.DataFrame(routes_data)
    payload_df = pd.DataFrame(payload_data)

    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        routes_df.to_excel(writer, sheet_name='routes', index=False)
        payload_df.to_excel(writer, sheet_name='route_payload', index=False)

    excel_file.seek(0)
    return excel_file


def test_import_endpoint(token, base_url):
    \"\"\"Prueba el endpoint de importación.\"\"\"

    print(f\"\\n{'='*60}\")
    print(\"Test de Endpoint de Importación de Rutas\")
    print(f\"{'='*60}\\n\")

    # Crear archivo de prueba
    print(\"1. Creando archivo Excel de prueba...\")\
    try:
        excel_file = create_test_excel()
        print(\"   ✓ Archivo Excel creado exitosamente\")\
    except Exception as e:
        print(f\"   ✗ Error al crear archivo: {e}\")\
        return False

    # Preparar solicitud
    url = f\"{base_url}/api/routes/import/\"\
    headers = {\
        'Authorization': f'Token {token}'\
    }\
    files = {\
        'file': ('test_routes.xlsx', excel_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),\
        'batch_name': (None, 'Test Batch'),\
    }\
    \
    print(f\"\\n2. Enviando solicitud POST a {url}\")\
    print(f\"   Headers: {headers}\")\
    print(f\"   Tipo: multipart/form-data\")\
    \
    # Enviar solicitud\
    try:\
        response = requests.post(url, files=files, headers=headers, timeout=10)\
        print(f\"   Status Code: {response.status_code}\")\
    except requests.exceptions.ConnectionError:\
        print(f\"   ✗ Error de conexión. ¿El servidor está en {base_url}?\")\
        return False\
    except Exception as e:\
        print(f\"   ✗ Error al enviar solicitud: {e}\")\
        return False\
    \
    # Mostrar respuesta\
    print(f\"\\n3. Respuesta del servidor:\")\
    try:\
        response_json = response.json()\
        print(f\"   Status: {response_json.get('status')}\")\
        \
        if response.status_code == 201:\
            print(\"   ✓ Importación exitosa (201 Created)\")\
            data = response_json.get('data', {})\
            print(f\"   - Batch ID: {data.get('batch_id')}\")\
            print(f\"   - Total registros: {data.get('total')}\")\
            print(f\"   - Registros válidos: {data.get('valid')}\")\
            print(f\"   - Registros inválidos: {data.get('invalid')}\")\
            \
            if data.get('errors'):\
                print(f\"\\n   Errores encontrados:\")\
                for error in data.get('errors', []):\
                    print(f\"     - Fila {error.get('row')}: {error.get('error')}\")\
            \
            return True\
        else:\
            print(f\"   ✗ Error: {response.status_code}\")\
            if 'errors' in response_json:\
                print(f\"   Detalles: {response_json.get('errors')}\")\
            elif 'message' in response_json:\
                print(f\"   Mensaje: {response_json.get('message')}\")\
            return False\
    except ValueError:\
        print(f\"   ✗ Respuesta no es JSON\")\
        print(f\"   Contenido: {response.text[:200]}\")\
        return False\
    \n\
    print(f\"\\n{'='*60}\\n\")\


def main():\
    if len(sys.argv) < 2:\
        print(__doc__)\
        print(\"\\nEjemplo:\")\
        print(\"  python test_import_endpoint.py 8b57ab78b769b0bb358c60b2eef025c6efc895a2 http://localhost:8000\")\
        sys.exit(1)\
    \
    token = sys.argv[1]\
    base_url = sys.argv[2] if len(sys.argv) > 2 else \"http://localhost:8000\"\
    \
    success = test_import_endpoint(token, base_url)\
    sys.exit(0 if success else 1)\


if __name__ == '__main__':\
    main()\
