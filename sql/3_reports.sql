CREATE TABLE IF NOT EXISTS reports (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    company_id integer NOT NULL REFERENCES companies(id),
    report_type text NOT NULL CHECK (report_type IN ('annual', 'quarterly')),
    report_date date NOT NULL,
    period_end date NOT NULL,
    shares bigint,
    net_income_parent numeric,
    total_equity numeric,
    dividend numeric,
    revenue numeric,
    assets numeric,
    debt numeric,
    currency text NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    UNIQUE (company_id, report_type, period_end)
);
