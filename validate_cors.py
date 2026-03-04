#!/usr/bin/env python
"""
Script de validación de CORS
Verifica que los headers de CORS estén siendo devueltos correctamente
"""

import os
import sys
import requests
from urllib.parse import urljoin

# Colores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(title):
    print(f"\n{BLUE}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{RESET}\n")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def validate_cors(api_url, origin):
    """Valida CORS haciendo un preflight request"""

    print_header(f"Validando CORS desde: {origin}")
    print_info(f"API URL: {api_url}")

    headers = {
        'Origin': origin,
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type, Authorization',
    }

    try:
        # Test OPTIONS request (preflight)
        print("\n1️⃣  Probando solicitud preflight (OPTIONS)...")
        response = requests.options(f"{api_url}/token-auth/", headers=headers, timeout=5)

        print_info(f"Status Code: {response.status_code}")

        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
            'Access-Control-Max-Age': response.headers.get('Access-Control-Max-Age'),
        }

        print("\nHeaders CORS recibidos:")
        for header, value in cors_headers.items():
            if value:
                print_success(f"  {header}: {value}")
            else:
                print_error(f"  {header}: FALTA")

        if cors_headers['Access-Control-Allow-Origin']:
            if cors_headers['Access-Control-Allow-Origin'] == origin or cors_headers['Access-Control-Allow-Origin'] == '*':
                print_success("✓ CORS preflight exitoso")
                return True
            else:
                print_error(f"✗ Origen no coincide. Esperado: {origin}, Recibido: {cors_headers['Access-Control-Allow-Origin']}")
                return False
        else:
            print_error("✗ Falta header Access-Control-Allow-Origin")
            return False

    except Exception as e:
        print_error(f"Error durante preflight: {str(e)}")
        return False

def main():
    # Configuración
    api_url = os.getenv('API_URL', 'http://localhost:8080/api')

    # Remover /api si está al final
    if api_url.endswith('/api'):
        api_url = api_url[:-4]

    origins = [
        'http://localhost:3000',
        'http://localhost:4200',
        'http://localhost:8000',
        'https://api.logistics.josetrespalaciosbedoya.co',
        'https://logistics.josetrespalaciosbedoya.co',
    ]

    print(f"\n{BLUE}╔═══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║       VALIDADOR DE CONFIGURACIÓN CORS - LOGISTICS        ║{RESET}")
    print(f"{BLUE}╚═══════════════════════════════════════════════════════════╝{RESET}")

    print(f"\nAPI URL: {BLUE}{api_url}{RESET}")

    results = []
    for origin in origins:
        result = validate_cors(api_url, origin)
        results.append((origin, result))

    # Resumen
    print_header("RESUMEN DE VALIDACIÓN")

    success_count = sum(1 for _, r in results if r)
    total_count = len(results)

    for origin, result in results:
        if result:
            print_success(f"{origin}: OK")
        else:
            print_error(f"{origin}: FAILED")

    print(f"\nResultado: {success_count}/{total_count} orígenes pasaron validación")

    if success_count == total_count:
        print_success("✓ Todas las configuraciones de CORS están correctas")
        return 0
    else:
        print_warning("⚠ Hay problemas con la configuración de CORS")
        return 1

if __name__ == '__main__':
    sys.exit(main())
