SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';

CREATE TABLE IF NOT EXISTS empty (
            id SERIAL PRIMARY KEY
        );

DROP TABLE IF EXISTS empty;