import psycopg


def store_shares(conn: psycopg.Connection, shares: list[dict]) -> None:
    companies = {s["lei"]: s["country"] for s in shares}
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO companies (lei, country) "
            "VALUES (%s, %s) "
            "ON CONFLICT (lei) DO NOTHING",
            companies.items(),
        )
        ids = dict(cur.execute("SELECT lei, id FROM companies").fetchall())
        securities = [
            (ids[s["lei"]], s["isin"], s["venue"], s["currency"], s["term_date"])
            for s in shares
        ]
        cur.executemany(
            "INSERT INTO securities (company_id, isin, venue, currency, inactive_date) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON CONFLICT (isin) DO NOTHING",
            securities,
        )
