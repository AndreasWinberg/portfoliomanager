from portfoliomanager.db import connect, create_schema
from portfoliomanager.universe import store_shares

shares = [
    {
        "lei": "TEST0000000000000001",
        "country": "SE",
        "isin": "SETEST000001",
        "venue": "XSTO",
        "currency": "SEK",
        "term_date": None,
    },
    {
        "lei": "TEST0000000000000001",
        "country": "SE",
        "isin": "SETEST000002",
        "venue": "XSTO",
        "currency": "SEK",
        "term_date": None,
    },
    {
        "lei": "TEST0000000000000002",
        "country": "SE",
        "isin": "SETEST000003",
        "venue": "XSTO",
        "currency": "SEK",
        "term_date": None,
    },
]


def _counts(conn) -> tuple[int, int]:
    companies = conn.execute(
        "SELECT count(*) FROM companies WHERE lei LIKE 'TEST%'"
    ).fetchone()[0]
    securities = conn.execute(
        "SELECT count(*) FROM securities WHERE isin LIKE 'SETEST%'"
    ).fetchone()[0]
    return companies, securities


def test_idempotent() -> None:
    with connect() as conn:
        create_schema(conn)
        store_shares(conn, shares)
        assert _counts(conn) == (2, 3)
        store_shares(conn, shares)
        assert _counts(conn) == (2, 3)
        conn.rollback()
        assert _counts(conn) == (0, 0)
