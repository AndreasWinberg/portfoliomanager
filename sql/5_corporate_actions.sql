CREATE TABLE IF NOT EXISTS corporate_actions (
    company_id integer NOT NULL REFERENCES companies(id),
    action_type text NOT NULL CHECK (action_type IN ('acquisition', 'bankruptcy', 'dividend', 'buyback', 'delisting')),
    amount numeric,
    action_date date NOT NULL,
    currency text CHECK (currency ~ '^[A-Z]{3}$'),
    CHECK (amount IS NULL OR currency IS NOT NULL),
    PRIMARY KEY (company_id, action_type, action_date)
);
