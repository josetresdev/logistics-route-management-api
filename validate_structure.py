#!/usr/bin/env python
"""
Script de validación de estructura MTV + DDD del proyecto.
Verifica que el proyecto cumple con el patrón Model-Template-View de Django
y Domain-Driven Design.
"""

import os
import sys
from pathlib import Path
import ast
import json

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_ok(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


class StructureValidator:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.info = []
        self.checks_passed = 0
        self.checks_failed = 0

    def check_file_exists(self, relative_path, description=""):
        """Verifica que un archivo existe."""
        file_path = self.base_path / relative_path
        if file_path.exists():
            self.checks_passed += 1
            desc = f" ({description})" if description else ""
            print_ok(f"{relative_path}{desc}")
            return True
        else:
            self.checks_failed += 1
            desc = f" ({description})" if description else ""
            print_error(f"{relative_path}{desc} - NOT FOUND")
            self.errors.append(f"File not found: {relative_path}")
            return False

    def check_file_contains(self, relative_path, search_str, description=""):
        """Verifica que un archivo contiene cierto texto."""
        file_path = self.base_path / relative_path
        if not file_path.exists():
            self.checks_failed += 1
            print_error(f"{relative_path} - FILE NOT FOUND")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if search_str in content:
                    self.checks_passed += 1
                    print_ok(f"{relative_path} contains '{search_str}'")
                    return True
                else:
                    self.checks_failed += 1
                    print_error(f"{relative_path} does NOT contain '{search_str}'")
                    self.errors.append(
                        f"{relative_path} missing: {search_str}"
                    )
                    return False
        except Exception as e:
            self.checks_failed += 1
            print_error(f"Error reading {relative_path}: {e}")
            return False

    def check_python_syntax(self, relative_path):
        """Valida sintaxis Python de un archivo."""
        file_path = self.base_path / relative_path
        if not file_path.exists():
            self.checks_failed += 1
            print_error(f"{relative_path} - FILE NOT FOUND")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            self.checks_passed += 1
            print_ok(f"{relative_path} - Python syntax valid")
            return True
        except SyntaxError as e:
            self.checks_failed += 1
            print_error(f"{relative_path} - Syntax Error: {e}")
            self.errors.append(f"Syntax error in {relative_path}: {e}")
            return False

    def validate_mtv_structure(self):
        """Valida la estructura MTV del proyecto."""
        print_header("VALIDATING MTV STRUCTURE")

        # MTV MODEL Layer
        print_info("MTV MODEL Layer (domain/models.py)")
        self.check_file_exists(
            "apps/routes/domain/models.py",
            "MTV: Model definition with ORM"
        )
        self.check_file_contains(
            "apps/routes/domain/models.py",
            "models.Model",
            "Inherits from Django models.Model"
        )

        # MTV TEMPLATE Layer
        print_info("\nMTV TEMPLATE Layer (api/serializers.py)")
        self.check_file_exists(
            "apps/routes/api/serializers.py",
            "MTV: Template for JSON serialization"
        )
        self.check_file_contains(
            "apps/routes/api/serializers.py",
            "serializers.ModelSerializer",
            "Uses DRF ModelSerializer"
        )

        # MTV VIEW Layer
        print_info("\nMTV VIEW Layer (api/views.py)")
        self.check_file_exists(
            "apps/routes/api/views.py",
            "MTV: View processing HTTP requests"
        )
        self.check_file_contains(
            "apps/routes/api/views.py",
            "viewsets.ModelViewSet",
            "Uses DRF ModelViewSet"
        )

        # MTV URL Routing
        print_info("\nMTV URL Routing (api/urls.py)")
        self.check_file_exists(
            "apps/routes/api/urls.py",
            "MTV: URL routing entry point"
        )
        self.check_file_contains(
            "apps/routes/api/urls.py",
            "DefaultRouter",
            "Uses DRF DefaultRouter"
        )

    def validate_ddd_layers(self):
        """Valida las capas DDD del proyecto."""
        print_header("VALIDATING DDD LAYERS")

        # Domain Layer
        print_info("DDD Domain Layer")
        self.check_file_exists(
            "apps/routes/domain/models.py",
            "Models and business entities"
        )
        self.check_file_exists(
            "apps/routes/domain/managers.py",
            "Custom QuerySets and Managers"
        )

        # Application Layer
        print_info("\nDDD Application Layer")
        self.check_file_exists(
            "apps/routes/application/services.py",
            "Business logic and use cases"
        )
        self.check_file_exists(
            "apps/routes/application/validators.py",
            "Business validation rules"
        )

        # Infrastructure Layer
        print_info("\nDDD Infrastructure Layer")
        self.check_file_exists(
            "apps/routes/infrastructure/repositories.py",
            "Data access abstraction"
        )

        # API/Presentation Layer
        print_info("\nDDD API/Presentation Layer")
        self.check_file_exists(
            "apps/routes/api/views.py",
            "HTTP request handling"
        )
        self.check_file_exists(
            "apps/routes/api/serializers.py",
            "Request/Response serialization"
        )
        self.check_file_exists(
            "apps/routes/api/filters.py",
            "Query filtering"
        )

    def validate_django_configuration(self):
        """Valida configuración de Django."""
        print_header("VALIDATING DJANGO CONFIGURATION")

        # Settings
        print_info("Django Settings")
        self.check_file_exists(
            "config/settings.py",
            "Django settings module"
        )
        self.check_file_contains(
            "config/settings.py",
            "INSTALLED_APPS",
            "INSTALLED_APPS configured"
        )
        self.check_file_contains(
            "config/settings.py",
            "apps.routes",
            "'apps.routes' app registered"
        )

        # URLs
        print_info("\nDjango URLs Configuration")
        self.check_file_exists(
            "config/urls.py",
            "Main URL configuration"
        )
        self.check_file_contains(
            "config/urls.py",
            "apps.routes.api.urls",
            "Routes app URLs included"
        )

        # WSGI
        print_info("\nWWSGI Configuration")
        self.check_file_exists(
            "config/wsgi.py",
            "WSGI application"
        )

    def validate_python_syntax(self):
        """Valida sintaxis Python de archivos críticos."""
        print_header("VALIDATING PYTHON SYNTAX")

        files_to_check = [
            "manage.py",
            "config/settings.py",
            "config/urls.py",
            "config/wsgi.py",
            "apps/__init__.py",
            "apps/routes/__init__.py",
            "apps/routes/domain/models.py",
            "apps/routes/application/services.py",
            "apps/routes/application/validators.py",
            "apps/routes/infrastructure/repositories.py",
            "apps/routes/api/views.py",
            "apps/routes/api/serializers.py",
            "apps/routes/api/urls.py",
            "apps/routes/api/filters.py",
        ]

        for file_path in files_to_check:
            self.check_python_syntax(file_path)

    def validate_requirements(self):
        """Valida que las dependencias estén listadas."""
        print_header("VALIDATING REQUIREMENTS")

        required_packages = [
            "Django",
            "djangorestframework",
            "psycopg2",
            "django-filter",
            "pandas",
            "gunicorn",
            "drf-spectacular",
        ]

        self.check_file_exists("requirements.txt", "Python dependencies")

        try:
            with open(self.base_path / "requirements.txt", 'r') as f:
                reqs_content = f.read().lower()
                for package in required_packages:
                    if package.lower() in reqs_content:
                        self.checks_passed += 1
                        print_ok(f"{package} - listed in requirements.txt")
                    else:
                        self.checks_failed += 1
                        print_warning(f"{package} - NOT found in requirements.txt")
                        self.warnings.append(f"Missing package: {package}")
        except Exception as e:
            self.checks_failed += 1
            print_error(f"Error reading requirements.txt: {e}")

    def validate_docker_setup(self):
        """Valida configuración Docker."""
        print_header("VALIDATING DOCKER CONFIGURATION")

        self.check_file_exists("Dockerfile", "Docker image definition")
        self.check_file_exists("docker-compose.yml", "Docker Compose dev config")
        self.check_file_exists("docker-compose.prod.yml", "Docker Compose prod config")
        self.check_file_exists("nginx.conf", "Nginx configuration")

    def validate_documentation(self):
        """Valida documentación con MTV pattern."""
        print_header("VALIDATING DOCUMENTATION")

        docs = [
            ("readme.md", "Project README"),
            ("QUICK_START.md", "Quick start guide"),
            ("INSTALL.md", "Installation guide"),
            ("STRUCTURE.md", "Project structure"),
            ("CONTRIBUTING.md", "Contributing guide"),
        ]

        for doc_file, description in docs:
            self.check_file_exists(doc_file, description)

        # Check MTV mention in README
        print_info("\nMTV Documentation in README")
        self.check_file_contains(
            "readme.md",
            "MTV",
            "MTV pattern documented"
        )
        self.check_file_contains(
            "readme.md",
            "Domain-Driven Design",
            "DDD pattern documented"
        )

    def validate_tests(self):
        """Valida estructura de tests."""
        print_header("VALIDATING TEST STRUCTURE")

        self.check_file_exists(
            "apps/routes/tests/__init__.py",
            "Tests module"
        )
        self.check_file_exists(
            "apps/routes/tests/test_api.py",
            "API tests"
        )

    def validate_exceptions(self):
        """Valida manejador de excepciones."""
        print_header("VALIDATING EXCEPTION HANDLING")

        self.check_file_exists(
            "apps/routes/exceptions.py",
            "Custom exceptions"
        )
        self.check_file_contains(
            "apps/routes/exceptions.py",
            "Exception",
            "Custom exception classes defined"
        )

    def generate_report(self):
        """Genera reporte final de validación."""
        print_header("VALIDATION SUMMARY REPORT")

        total_checks = self.checks_passed + self.checks_failed
        success_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0

        print_info(f"Total Checks: {total_checks}")
        print_ok(f"Passed: {self.checks_passed}")
        print_error(f"Failed: {self.checks_failed}")
        print_info(f"Success Rate: {success_rate:.1f}%")

        if self.errors:
            print_header("ERRORS FOUND")
            for error in self.errors:
                print_error(error)

        if self.warnings:
            print_header("WARNINGS")
            for warning in self.warnings:
                print_warning(warning)

        print_header("PROJECT STRUCTURE VALIDATION")

        if self.checks_failed == 0:
            print_ok("✓ MTV Structure is properly implemented!")
            print_ok("✓ DDD Layers are correctly organized!")
            print_ok("✓ Django configuration is complete!")
            print_ok("✓ All required files are present!")
            return True
        else:
            print_error("✗ Some validation checks failed!")
            print_error(f"✗ Please review the errors above and fix them.")
            return False

    def run_all_validations(self):
        """Ejecuta todas las validaciones."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  LOGISTICS ROUTE MANAGEMENT API - PROJECT VALIDATOR      ║")
        print("║              MTV + DDD Structure Validation                ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")

        self.validate_mtv_structure()
        self.validate_ddd_layers()
        self.validate_django_configuration()
        self.validate_python_syntax()
        self.validate_requirements()
        self.validate_docker_setup()
        self.validate_documentation()
        self.validate_tests()
        self.validate_exceptions()

        success = self.generate_report()
        return success


def main():
    """Punto de entrada del validador."""
    base_path = Path(__file__).parent
    validator = StructureValidator(base_path)
    success = validator.run_all_validations()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
