CREATE TABLE IF NOT EXISTS securities (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    company_id integer NOT NULL REFERENCES companies(id),
    isin text NOT NULL UNIQUE CHECK (isin ~ '^[A-Z]{2}[A-Z0-9]{9}[0-9]$'),
    ticker text,
    venue text NOT NULL,
    currency text NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    inactive_date date
);
