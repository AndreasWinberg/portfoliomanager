CREATE TABLE IF NOT EXISTS prices (
    company_id integer REFERENCES companies(id),
    price_date date,
    close_price numeric NOT NULL,
    volume bigint,
    currency text NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    PRIMARY KEY (company_id, price_date)
);
