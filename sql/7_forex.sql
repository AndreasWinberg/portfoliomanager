CREATE TABLE IF NOT EXISTS forex (
    forex_date date,
    currency text CHECK (currency ~ '^[A-Z]{3}$'),
    per_euro_rate numeric NOT NULL,
    CHECK (per_euro_rate > 0),
    PRIMARY KEY (currency, forex_date)
);
