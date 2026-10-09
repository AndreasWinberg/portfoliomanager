CREATE TABLE IF NOT EXISTS splits (
    company_id integer REFERENCES companies(id),
    split_date date,
    split_ratio numeric NOT NULL,
    PRIMARY KEY (company_id, split_date)
);
