CREATE TABLE scale_readings (
    scale_id VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    PRIMARY KEY (scale_id, timestamp)
);