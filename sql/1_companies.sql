CREATE TABLE IF NOT EXISTS companies (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    lei text NOT NULL UNIQUE CHECK (lei ~ '^[A-Z0-9]{18}[0-9]{2}$'),
    sector text,
    name text,
    country text CHECK (country ~ '^[A-Z]{2}$'),
    inactive_date date
);
