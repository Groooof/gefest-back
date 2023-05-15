CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL,
    is_superuser BOOL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    token UUID PRIMARY KEY,
    expires_in TIMESTAMP NOT NULL,
    user_id UUID NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO users (username, hashed_password, role, is_superuser)
VALUES ('admin', crypt('admin', gen_salt('bf', 10)), 'common', TRUE);
