#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para validar que el archivo dataset.xlsx matchee con la solución del endpoint.
"""

import pandas as pd
import sys
from pathlib import Path


# Configurar encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def validate_excel(filepath):
    """Valida la estructura y contenido del archivo Excel."""

    print("=" * 70)
    print("VALIDACIÓN DE ARCHIVO EXCEL - dataset.xlsx")
    print("=" * 70)

    # 1. Verificar que el archivo existe
    if not Path(filepath).exists():
        print(f"❌ CRÍTICO: Archivo no encontrado: {filepath}")
        return False

    print(f"\n✅ Archivo encontrado: {filepath}")
    print(f"   Tamaño: {Path(filepath).stat().st_size / 1024:.1f} KB")

    # 2. Leer hojas
    try:
        excel_file = pd.ExcelFile(filepath)
        hojas = excel_file.sheet_names
        print(f"\n📄 Hojas disponibles: {hojas}")
    except Exception as e:
        print(f"❌ Error al leer hojas: {e}")
        return False

    # 3. Validar hojas requeridas
    hojas_requeridas = ['routes', 'route_payload']
    hojas_faltantes = [h for h in hojas_requeridas if h not in hojas]

    if hojas_faltantes:
        print(f"\n❌ CRÍTICO: Faltan hojas: {hojas_faltantes}")
        print(f"   Se esperan: {hojas_requeridas}")
        print(f"   Se encontraron: {hojas}")
        return False

    print(f"\n✅ Todas las hojas requeridas presentes")

    # 4. Leer hoja "routes"
    try:
        routes_df = pd.read_excel(filepath, sheet_name='routes')
        print(f"\n📊 Hoja 'routes':")
        print(f"   Registros: {len(routes_df)}")
        print(f"   Columnas: {list(routes_df.columns)}")
    except Exception as e:
        print(f"❌ Error al leer hoja 'routes': {e}")
        return False

    # 5. Leer hoja "route_payload"
    try:
        payload_df = pd.read_excel(filepath, sheet_name='route_payload')
        print(f"\n📊 Hoja 'route_payload':")
        print(f"   Registros: {len(payload_df)}")
        print(f"   Columnas: {list(payload_df.columns)}")
    except Exception as e:
        print(f"❌ Error al leer hoja 'route_payload': {e}")
        return False

    # 6. Validar columnas requeridas en "routes"
    # Normalizar nombres de columna
    routes_df_normalized = routes_df.copy()
    routes_df_normalized.columns = [str(c).strip().lower() for c in routes_df_normalized.columns]

    # Columnas requeridas (puede ser idroute o id_route)
    columnas_requeridas_routes = [
        'origin', 'destination', 'distance_km',
        'priority', 'time_window_start', 'time_window_end', 'status'
    ]

    # Columnas alternativas para ID
    columnas_id = ['id_route', 'idroute']
    tiene_id = any(c in routes_df_normalized.columns for c in columnas_id)

    columnas_faltantes = [c for c in columnas_requeridas_routes if c not in routes_df_normalized.columns]

    print(f"\n🔍 Validación de columnas en 'routes':")
    print(f"   Columnas disponibles: {list(routes_df_normalized.columns)}")

    if not tiene_id:
        print(f"   ❌ CRÍTICO: Falta columna ID (esperaba 'id_route' o 'idroute')")
        return False

    if columnas_faltantes:
        print(f"   ❌ CRÍTICO: Faltan columnas: {columnas_faltantes}")
        return False
    else:
        print(f"   ✅ Todas las columnas requeridas presentes:")
        for col in columnas_requeridas_routes:
            print(f"      ✓ {col}")

        id_col = next((c for c in columnas_id if c in routes_df_normalized.columns), None)
        print(f"      ✓ {id_col} (ID)")

        # Guardar el nombre de la columna ID para uso posterior
        globals()['id_col_name'] = id_col
    # 7. Validar columnas requeridas en "route_payload"
    # Columnas alternativas para ID
    columnas_id_payload = ['id_route', 'idroute']

    payload_df_normalized = payload_df.copy()
    payload_df_normalized.columns = [str(c).strip().lower() for c in payload_df_normalized.columns]

    tiene_id_payload = any(c in payload_df_normalized.columns for c in columnas_id_payload)

    print(f"\n🔍 Validación de columnas en 'route_payload':")
    print(f"   Columnas disponibles: {list(payload_df_normalized.columns)}")

    if not tiene_id_payload:
        print(f"   ❌ CRÍTICO: Falta columna ID (esperaba 'id_route' o 'idroute')")
        return False
    else:
        print(f"   ✅ Todas las columnas requeridas presentes:")
        id_col_payload = next((c for c in columnas_id_payload if c in payload_df_normalized.columns), None)
        print(f"      ✓ {id_col_payload} (ID)")

        if 'payload' in payload_df_normalized.columns:
            print(f"      ✓ payload (opcional)")
    # 8. Validar datos
    print(f"\n🔍 Validación de datos en 'routes':")

    validation_errors = []

    # Verificar registros vacíos
    if routes_df_normalized.isnull().all(axis=1).any():
        validation_errors.append("❌ Hay filas completamente vacías")

    # Validar que origin y destination no sean nulos
    null_origin = routes_df_normalized['origin'].isnull().sum()
    null_destination = routes_df_normalized['destination'].isnull().sum()

    if null_origin > 0:
        validation_errors.append(f"❌ {null_origin} registros con 'origin' nulo")
    if null_destination > 0:
        validation_errors.append(f"❌ {null_destination} registros con 'destination' nulo")

    # Validar distance_km > 0
    try:
        distance_km = pd.to_numeric(routes_df_normalized['distance_km'], errors='coerce')
        invalid_distances = (distance_km <= 0).sum()
        null_distances = distance_km.isnull().sum()

        if null_distances > 0:
            validation_errors.append(f"❌ {null_distances} registros con 'distance_km' nulo")
        if invalid_distances > 0:
            validation_errors.append(f"❌ {invalid_distances} registros con 'distance_km' <= 0")
    except Exception as e:
        validation_errors.append(f"❌ Error validando distance_km: {e}")

    # Validar priority > 0
    try:
        priority = pd.to_numeric(routes_df_normalized['priority'], errors='coerce')
        invalid_priority = (priority <= 0).sum()
        null_priority = priority.isnull().sum()

        if null_priority > 0:
            validation_errors.append(f"❌ {null_priority} registros con 'priority' nulo")
        if invalid_priority > 0:
            validation_errors.append(f"❌ {invalid_priority} registros con 'priority' <= 0")
    except Exception as e:
        validation_errors.append(f"❌ Error validando priority: {e}")

    # Validar ventana de tiempo
    try:
        start_times = pd.to_datetime(routes_df_normalized['time_window_start'], errors='coerce')
        end_times = pd.to_datetime(routes_df_normalized['time_window_end'], errors='coerce')

        null_starts = start_times.isnull().sum()
        null_ends = end_times.isnull().sum()
        invalid_windows = (start_times >= end_times).sum()

        if null_starts > 0:
            validation_errors.append(f"❌ {null_starts} registros con 'time_window_start' nulo o inválido")
        if null_ends > 0:
            validation_errors.append(f"❌ {null_ends} registros con 'time_window_end' nulo o inválido")
        if invalid_windows > 0:
            validation_errors.append(f"❌ {invalid_windows} registros con ventana de tiempo inválida (start >= end)")
    except Exception as e:
        validation_errors.append(f"❌ Error validando ventanas de tiempo: {e}")

    # Validar status no sea nulo
    null_status = routes_df_normalized['status'].isnull().sum()
    if null_status > 0:
        validation_errors.append(f"❌ {null_status} registros con 'status' nulo")

    if validation_errors:
        for error in validation_errors:
            print(f"   {error}")
    else:
        print(f"   ✅ Todos los datos son válidos")

    # 9. Validar match entre routes y route_payload
    print(f"\n🔍 Validación de match entre hojas:")

    # Encontrar las columnas ID
    id_cols = ['id_route', 'idroute']
    routes_id_col = next((c for c in id_cols if c in routes_df_normalized.columns), None)
    payload_id_col = next((c for c in id_cols if c in payload_df_normalized.columns), None)

    if not routes_id_col or not payload_id_col:
        print(f"   ❌ No se encontraron columnas ID")
        return False

    routes_ids = set(routes_df_normalized[routes_id_col].unique())
    payload_ids = set(payload_df_normalized[payload_id_col].unique())

    ids_en_payload_no_en_routes = payload_ids - routes_ids
    ids_en_routes_no_en_payload = routes_ids - payload_ids

    if ids_en_payload_no_en_routes:
        print(f"   ⚠️  IDs en 'route_payload' que no están en 'routes': {len(ids_en_payload_no_en_routes)} registros")

    if not ids_en_payload_no_en_routes and not ids_en_routes_no_en_payload:
        print(f"   ✅ Perfect match entre routes y route_payload")
    elif not ids_en_payload_no_en_routes:
        print(f"   ✅ Todos los payloads corresponden a rutas válidas")

    # 10. Resumen
    print(f"\n{'='*70}")
    print("RESUMEN")
    print(f"{'='*70}")

    if not validation_errors and not ids_en_payload_no_en_routes:
        print(f"✅ VALIDACIÓN EXITOSA")
        print(f"\n   El archivo dataset.xlsx es compatible con la solución.")
        print(f"   • Hojas: {', '.join(hojas_requeridas)}")
        print(f"   • Registros en 'routes': {len(routes_df)}")
        print(f"   • Registros en 'route_payload': {len(payload_df)}")
        print(f"   • Todos los datos son válidos")
        return True
    else:
        if validation_errors:
            print(f"❌ VALIDACIÓN CON ERRORES")
            print(f"\n   Por favor, corrige los siguientes problemas:")
            for i, error in enumerate(validation_errors, 1):
                print(f"   {i}. {error}")

        if ids_en_payload_no_en_routes:
            print(f"\n❌ MISMATCH EN IDs")
            print(f"   {len(ids_en_payload_no_en_routes)} IDs en payload no existen en routes")

        return False


if __name__ == '__main__':
    filepath = 'dataset.xlsx'
    success = validate_excel(filepath)
    sys.exit(0 if success else 1)
