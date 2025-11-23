import os
from typing import List, Tuple, Any

import duckdb
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DUCKDB_PATH = os.getenv("DUCKDB_PATH", "demo.db")


def _run_postgres(sql: str) -> Tuple[List[str], List[List[Any]]]:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
    finally:
        conn.close()

    return columns, rows


def _run_duckdb(sql: str) -> Tuple[List[str], List[List[Any]]]:
    conn = duckdb.connect(DUCKDB_PATH)
    try:
        result = conn.execute(sql)
        rows = result.fetchall()
        columns = [col[0] for col in result.description]
    finally:
        conn.close()

    return columns, rows


def run_query(sql: str) -> Tuple[List[str], List[List[Any]]]:
    stripped = sql.strip().lower()
    if not stripped.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    if DATABASE_URL:
        return _run_postgres(sql)
    else:
        return _run_duckdb(sql)
