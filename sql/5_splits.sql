CREATE TABLE IF NOT EXISTS splits (
    security_id integer REFERENCES securities(id),
    split_date date,
    split_ratio numeric NOT NULL,
    PRIMARY KEY (security_id, split_date)
);
