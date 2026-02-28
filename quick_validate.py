#!/usr/bin/env python
"""
MTV + DDD Quick Validator
Validación rápida y visual de la estructura del proyecto
"""

import subprocess
import sys

def run_command(cmd):
    """Ejecuta un comando y retorna el resultado."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_file_exists(path):
    """Verifica si un archivo existe."""
    import os
    return os.path.exists(path)


def check_file_contains(path, text):
    """Verifica si un archivo contiene cierto texto (case-insensitive)."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return text.lower() in f.read().lower()
    except Exception:
        return False


def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     MTV + DDD STRUCTURE QUICK VALIDATOR                   ║")
    print("║        Logistics Route Management API                     ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    tests = {
        "MTV Components": [
            ("Model: domain/models.py exists",
             lambda: check_file_exists("apps/routes/domain/models.py")),
            ("Model: inherits models.Model",
             lambda: check_file_contains("apps/routes/domain/models.py", "models.Model")),

            ("Template: api/serializers.py exists",
             lambda: check_file_exists("apps/routes/api/serializers.py")),
            ("Template: uses ModelSerializer",
             lambda: check_file_contains("apps/routes/api/serializers.py", "ModelSerializer")),

            ("View: api/views.py exists",
             lambda: check_file_exists("apps/routes/api/views.py")),
            ("View: uses ViewSet",
             lambda: check_file_contains("apps/routes/api/views.py", "viewsets.ModelViewSet")),

            ("URL: routing configured",
             lambda: check_file_exists("apps/routes/api/urls.py")),
            ("URL: uses DefaultRouter",
             lambda: check_file_contains("apps/routes/api/urls.py", "DefaultRouter")),
        ],

        "DDD Layers": [
            ("Domain: models.py present",
             lambda: check_file_exists("apps/routes/domain/models.py")),
            ("Domain: managers.py present",
             lambda: check_file_exists("apps/routes/domain/managers.py")),

            ("Application: services.py present",
             lambda: check_file_exists("apps/routes/application/services.py")),
            ("Application: validators.py present",
             lambda: check_file_exists("apps/routes/application/validators.py")),

            ("Infrastructure: repositories.py present",
             lambda: check_file_exists("apps/routes/infrastructure/repositories.py")),

            ("Presentation: views.py present",
             lambda: check_file_exists("apps/routes/api/views.py")),
        ],

        "Django Setup": [
            ("settings.py configured",
             lambda: check_file_exists("config/settings.py")),
            ("INSTALLED_APPS has 'routes'",
             lambda: check_file_contains("config/settings.py", "apps.routes")),

            ("urls.py includes app urls",
             lambda: check_file_contains("config/urls.py", "apps.routes.api.urls")),

            ("manage.py entry point",
             lambda: check_file_exists("manage.py")),
            ("wsgi.py configured",
             lambda: check_file_exists("config/wsgi.py")),
        ],

        "Support Files": [
            ("requirements.txt present",
             lambda: check_file_exists("requirements.txt")),
            ("Django in requirements",
             lambda: check_file_contains("requirements.txt", "Django")),
            ("DRF in requirements",
             lambda: check_file_contains("requirements.txt", "djangorestframework")),

            ("Docker configured",
             lambda: check_file_exists("Dockerfile")),
            ("docker-compose configured",
             lambda: check_file_exists("docker-compose.yml")),

            ("Documentation: README",
             lambda: check_file_exists("readme.md")),
            ("Documentation: MTV in README",
             lambda: check_file_contains("readme.md", "MTV")),
        ],
    }

    total_passed = 0
    total_tests = 0

    for category, category_tests in tests.items():
        print(f"\n📚 {category}")
        print("-" * 60)

        for test_name, test_func in category_tests:
            total_tests += 1
            try:
                result = test_func()
                if result:
                    print(f"   ✅ {test_name}")
                    total_passed += 1
                else:
                    print(f"   ❌ {test_name}")
            except Exception as e:
                print(f"   ❌ {test_name} (Error: {e})")

    print("\n" + "="*60)

    percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print(f"\nResults: {total_passed}/{total_tests} tests passed ({percentage:.0f}%)")

    if total_passed == total_tests:
        print("\n🎉 SUCCESS! Project structure is MTV + DDD compliant!")
        print("\n✅ All components are properly implemented:")
        print("   • MTV Pattern (Model-Template-View)")
        print("   • DDD Architecture (Domain-Driven Design)")
        print("   • Django Configuration")
        print("   • Dependencies & Support Files")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    print("\n")
    sys.exit(exit_code)
