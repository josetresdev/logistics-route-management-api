-- =========================================================
-- SCHEMA: logistics
-- Contiene todo el modelo relacional del sistema
-- =========================================================

CREATE SCHEMA IF NOT EXISTS logistics;
SET search_path TO logistics;


-- =========================================================
-- TABLA: route_status
-- Catálogo controlado para el campo status de routes
-- =========================================================

CREATE TABLE route_status (
    id          SMALLSERIAL PRIMARY KEY,
    code        VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- TABLA: priority_catalog
-- Catálogo controlado para el campo priority de routes
-- =========================================================

CREATE TABLE priority_catalog (
    id          SMALLSERIAL PRIMARY KEY,
    level       INTEGER UNIQUE NOT NULL CHECK (level > 0),
    description VARCHAR(100),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- TABLA: geographic_locations
-- Almacena información geográfica normalizada
-- Será referenciada por origin y destination
-- =========================================================

CREATE TABLE geographic_locations (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    address     TEXT NOT NULL,
    latitude    NUMERIC(9,6) NOT NULL,
    longitude   NUMERIC(9,6) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_lat CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT valid_lng CHECK (longitude BETWEEN -180 AND 180)
);


-- =========================================================
-- TABLA: import_batches
-- Permite trazabilidad de cargas masivas desde Excel
-- =========================================================

CREATE TABLE import_batches (
    id            BIGSERIAL PRIMARY KEY,
    file_name     VARCHAR(255) NOT NULL,
    total_rows    INTEGER,
    valid_rows    INTEGER,
    invalid_rows  INTEGER,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- TABLA PRINCIPAL: routes
-- Mantiene exactamente los nombres solicitados en la prueba
-- Contiene reglas estructurales críticas
-- =========================================================

CREATE TABLE routes (
    id                  BIGSERIAL PRIMARY KEY,

    origin              BIGINT NOT NULL REFERENCES geographic_locations(id),
    destination         BIGINT NOT NULL REFERENCES geographic_locations(id),

    distance_km         NUMERIC(10,2) NOT NULL CHECK (distance_km > 0),

    priority            SMALLINT NOT NULL REFERENCES priority_catalog(id),

    time_window_start   TIMESTAMP NOT NULL,
    time_window_end     TIMESTAMP NOT NULL,

    status              SMALLINT NOT NULL REFERENCES route_status(id),

    batch_id            BIGINT REFERENCES import_batches(id),

    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_time_window
        CHECK (time_window_start < time_window_end),

    CONSTRAINT unique_route_combination
        UNIQUE (
            origin,
            destination,
            time_window_start,
            time_window_end
        )
);


-- =========================================================
-- TABLA: route_payload
-- Almacena el JSON proveniente del Excel
-- Soporta variaciones estructurales
-- =========================================================

CREATE TABLE route_payload (
    id          BIGSERIAL PRIMARY KEY,
    route_id    BIGINT NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- TABLA: execution_logs
-- Auditoría de ejecución de rutas
-- Nombre conservado exactamente como lo pide la prueba
-- =========================================================

CREATE TABLE execution_logs (
    id              BIGSERIAL PRIMARY KEY,
    route_id        BIGINT NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    execution_time  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    result          VARCHAR(30) NOT NULL,
    message         TEXT,
    execution_ms    INTEGER,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- DATOS INICIALES
-- =========================================================

-- Estados de rutas
INSERT INTO route_status (code, description) VALUES
    ('PENDING', 'Ruta pendiente de ejecución'),
    ('IN_PROGRESS', 'Ruta en ejecución'),
    ('COMPLETED', 'Ruta completada exitosamente'),
    ('FAILED', 'Ruta con error'),
    ('CANCELLED', 'Ruta cancelada');

-- Prioridades
INSERT INTO priority_catalog (level, description) VALUES
    (1, 'Baja'),
    (2, 'Media'),
    (3, 'Alta'),
    (4, 'Crítica');

-- Ubicaciones geográficas de ejemplo
INSERT INTO geographic_locations (name, address, latitude, longitude) VALUES
    ('Centro Santiago', 'Avenida Libertador Bernardo O''Higgins 1449, Santiago', -33.438570, -70.665470),
    ('Estación Mapocho', 'Mapocho 21, Santiago', -33.435753, -70.660122),
    ('Parque Arauco', 'Avenida Presidente Kennedy 5413, Las Condes', -33.400622, -70.591905),
    ('La Moneda', 'Teatinos 120, Santiago', -33.440069, -70.668779);
