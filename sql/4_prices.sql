CREATE TABLE IF NOT EXISTS prices (
    security_id integer REFERENCES securities(id),
    price_date date,
    close_price numeric NOT NULL,
    volume bigint,
    currency text NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    PRIMARY KEY (security_id, price_date)
);
