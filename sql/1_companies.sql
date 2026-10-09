CREATE TABLE IF NOT EXISTS companies (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    isin text NOT NULL UNIQUE CHECK (isin ~ '^[A-Z]{2}[A-Z0-9]{9}[0-9]$'),
    ticker text NOT NULL,
    sector text NOT NULL,
    country text NOT NULL CHECK (country ~ '^[A-Z]{2}$'),
    venue text NOT NULL,
    currency text NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    inactive_date date
);
