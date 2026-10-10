import os
from pathlib import Path

import psycopg


def connect() -> psycopg.Connection:
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def create_schema(conn: psycopg.Connection) -> None:
    path = Path(__file__).parents[2] / "sql"
    for sql_file in sorted(path.glob("*.sql")):
        conn.execute(sql_file.read_text())
