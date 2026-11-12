CREATE TABLE leituras (
    time           TIMESTAMPTZ NOT NULL,
    bomba          TEXT NOT NULL,
    velocidade_hz  DOUBLE PRECISION,
    caudal_m3h     DOUBLE PRECISION,
    pressao_bar    DOUBLE PRECISION,
    potencia_kw    DOUBLE PRECISION
);

SELECT create_hypertable('leituras', 'time');