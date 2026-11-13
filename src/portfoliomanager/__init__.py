from pathlib import Path

from portfoliomanager import db, firds, universe


def main() -> int:
    shares, invalid = firds.latest_shares(Path("data"))
    with db.connect() as conn:
        db.create_schema(conn)
        universe.store_shares(conn, shares)
    print(f"{len(shares)} shares, {invalid} invalid")
    return 0
