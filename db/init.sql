-- =========================================================
-- Routes App Tables Only
-- Django creates all core tables during migrations
-- =========================================================

CREATE TABLE IF NOT EXISTS routes_location (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_routes_location_name ON routes_location(name);
CREATE INDEX IF NOT EXISTS idx_routes_location_coordinates ON routes_location(latitude, longitude);

CREATE TABLE IF NOT EXISTS routes_status (
    id SMALLSERIAL PRIMARY KEY,
    code VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_routes_status_code ON routes_status(code);

CREATE TABLE IF NOT EXISTS routes_import_batch (
    id BIGSERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    total_records INTEGER,
    valid_records INTEGER,
    invalid_records INTEGER,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_routes_import_batch_status ON routes_import_batch(status);
CREATE INDEX IF NOT EXISTS idx_routes_import_batch_created_at ON routes_import_batch(created_at);

CREATE TABLE IF NOT EXISTS routes_route (
    id BIGSERIAL PRIMARY KEY,
    origin_id BIGINT NOT NULL REFERENCES routes_location(id),
    destination_id BIGINT NOT NULL REFERENCES routes_location(id),
    distance_km NUMERIC(10,2) NOT NULL
        CONSTRAINT ck_routes_route_distance_km CHECK (distance_km > 0),
    priority INTEGER NOT NULL
        CONSTRAINT ck_routes_route_priority CHECK (priority > 0),
    time_window_start TIMESTAMP NOT NULL,
    time_window_end TIMESTAMP NOT NULL,
    status_id SMALLINT REFERENCES routes_status(id),
    batch_id BIGINT REFERENCES routes_import_batch(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_routes_route_time_window CHECK (time_window_start < time_window_end),
    CONSTRAINT uq_routes_route_combination UNIQUE (
        origin_id,
        destination_id,
        time_window_start,
        time_window_end
    )
);
CREATE INDEX IF NOT EXISTS idx_routes_route_origin_id ON routes_route(origin_id);
CREATE INDEX IF NOT EXISTS idx_routes_route_destination_id ON routes_route(destination_id);
CREATE INDEX IF NOT EXISTS idx_routes_route_status_id ON routes_route(status_id);
CREATE INDEX IF NOT EXISTS idx_routes_route_batch_id ON routes_route(batch_id);
CREATE INDEX IF NOT EXISTS idx_routes_route_created_at ON routes_route(created_at);

CREATE TABLE IF NOT EXISTS routes_payload (
    id BIGSERIAL PRIMARY KEY,
    route_id BIGINT NOT NULL REFERENCES routes_route(id) ON DELETE CASCADE,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_routes_payload_route_id ON routes_payload(route_id);
CREATE INDEX IF NOT EXISTS idx_routes_payload_created_at ON routes_payload(created_at);

CREATE TABLE IF NOT EXISTS routes_execution_log (
    id BIGSERIAL PRIMARY KEY,
    route_id BIGINT NOT NULL REFERENCES routes_route(id) ON DELETE CASCADE,
    execution_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    result VARCHAR(30) NOT NULL,
    message TEXT,
    execution_ms INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_routes_execution_log_route_id ON routes_execution_log(route_id);
CREATE INDEX IF NOT EXISTS idx_routes_execution_log_execution_time ON routes_execution_log(execution_time);
CREATE INDEX IF NOT EXISTS idx_routes_execution_log_created_at ON routes_execution_log(created_at);

-- =========================================================
-- INITIAL DATA
-- =========================================================

-- Route Status
INSERT INTO routes_status (code, description) VALUES
    ('PENDING', 'Ruta pendiente'),
    ('IN_PROGRESS', 'Ruta en ejecución'),
    ('READY', 'Lista para ejecución'),
    ('EXECUTED', 'Ejecutada'),
    ('FAILED', 'Fallida'),
    ('COMPLETED', 'Completada'),
    ('CANCELLED', 'Cancelada')
ON CONFLICT (code) DO NOTHING;

