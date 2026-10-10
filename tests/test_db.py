from portfoliomanager import db


def test_schema() -> None:
    with db.connect() as conn:
        db.create_schema(conn)
        query = (
            "SELECT table_name "
            "FROM information_schema.tables "
            "WHERE table_schema = 'public';"
        )
        rows = conn.execute(query).fetchall()

    names = {row[0] for row in rows}

    assert names == {"companies", "reports", "prices", "splits", "corporate_actions"}
