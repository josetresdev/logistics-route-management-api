.PHONY: help install run migrate shell superuser clean test lint docker build

help:
	@echo "📚 Logistics Route Management API - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          - Install dependencies and setup project"
	@echo "  make migrate          - Apply database migrations"
	@echo "  make superuser        - Create superuser for admin"
	@echo ""
	@echo "Development:"
	@echo "  make run              - Start development server (port 8000)"
	@echo "  make shell            - Open Django shell"
	@echo "  make createsuperuser  - Create admin user"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test             - Run all tests"
	@echo "  make lint             - Run linting (flake8)"
	@echo "  make coverage         - Run tests with coverage report"
	@echo ""
	@echo "Database:"
	@echo "  make flush            - Flush database (WARNING: deletes all data)"
	@echo "  make reset            - Reset migrations"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run Docker container"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            - Clean cache and temporary files"
	@echo "  make requirements     - Generate requirements.txt"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

migrate:
	@echo "🗄️  Applying migrations..."
	python manage.py migrate
	@echo "✅ Migrations applied!"

superuser:
	python manage.py createsuperuser

run:
	@echo "🚀 Starting development server..."
	@echo "📍 Access at: http://localhost:8000/api/"
	@echo "📍 Admin at: http://localhost:8000/admin/"
	python manage.py runserver 0.0.0.0:8000

shell:
	python manage.py shell

test:
	@echo "🧪 Running tests..."
	python manage.py test apps.routes

coverage:
	@echo "📊 Running tests with coverage..."
	coverage run --source='apps' manage.py test apps.routes
	coverage report
	coverage html
	@echo "✅ Coverage report generated in htmlcov/index.html"

lint:
	@echo "🔍 Running linting..."
	flake8 apps config --max-line-length=100
	@echo "✅ Linting complete!"

clean:
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '.DS_Store' -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	@echo "✅ Cleanup complete!"

flush:
	@echo "⚠️  WARNING: This will delete all database data!"
	python manage.py flush

reset:
	@echo "🔄 Resetting migrations..."
	python manage.py migrate apps.routes zero

requirements:
	@echo "📋 Generating requirements.txt..."
	pip freeze > requirements.txt
	@echo "✅ requirements.txt generated!"

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t logistics-api:latest .
	@echo "✅ Docker image built!"

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8000:8000 -e DEBUG=False logistics-api:latest
	@echo "📍 Container running at: http://localhost:8000/"

collectstatic:
	@echo "📁 Collecting static files..."
	python manage.py collectstatic --noinput
	@echo "✅ Static files collected!"

makemigrations:
	@echo "📝 Creating migrations..."
	python manage.py makemigrations

createsuperuser:
	python manage.py createsuperuser

check:
	@echo "🔍 Checking Django configuration..."
	python manage.py check
	@echo "✅ Configuration is OK!"
