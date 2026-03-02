FROM python:3.10-slim

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files (entrypoint.sh está en la raíz)
COPY . .

# 🔥 Elimina CRLF si viene desde Windows
RUN sed -i 's/\r$//' /app/entrypoint.sh

# 🔥 Permisos correctos
RUN chmod 755 /app/entrypoint.sh

# Create required directories
RUN mkdir -p logs media staticfiles

# Expose port
EXPOSE 8080

# 🔥 Ejecutar siempre con sh para evitar error binario
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
