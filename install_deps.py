#!/usr/bin/env python
"""
Script de instalación rápida de dependencias
Soluciona el error "Could not be resolved" de Pylance
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Instala todas las dependencias del proyecto."""

    print("\n" + "="*70)
    print("  INSTALADOR DE DEPENDENCIAS - Logistics Route Management API")
    print("="*70 + "\n")

    base_path = Path(__file__).parent
    requirements_file = base_path / "requirements.txt"

    if not requirements_file.exists():
        print("❌ requirements.txt no encontrado!")
        sys.exit(1)

    print("📦 Instalando dependencias desde requirements.txt...\n")

    try:
        # Upgrade pip
        print("[1/3] Actualizando pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip actualizado\n")

        # Install requirements
        print("[2/3] Instalando paquetes del proyecto...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✅ Paquetes instalados\n")

        # Verify python-dotenv
        print("[3/3] Verificando python-dotenv...")
        try:
            import dotenv
            print(f"✅ python-dotenv {dotenv.__version__} instalado correctamente\n")
        except ImportError:
            print("❌ python-dotenv no pudo ser instalado\n")
            sys.exit(1)

        print("="*70)
        print("  ✅ INSTALACIÓN EXITOSA")
        print("="*70)
        print("\n🎯 Próximos pasos:\n")
        print("1. En VS Code, presiona Ctrl+Shift+P (o Cmd+Shift+P en Mac)")
        print("2. Busca 'Python: Select Interpreter'")
        print("3. Elige el intérprete del venv actual")
        print("4. VS Code recargará el índice de Pylance")
        print("5. El error desaparecerá ✅\n")
        print("O para forzar el reload:")
        print("   - File > Reload Window (Ctrl+R)")
        print("   - Comando: Developer: Reload Window\n")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la instalación: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    install_dependencies()
