import os
from typing import List, Tuple, Any

import duckdb
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DUCKDB_PATH = os.getenv("DUCKDB_PATH", "demo.db")


def _run_postgres(sql: str) -> Tuple[List[str], List[List[Any]]]:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set but Postgres was selected")

    # psycopg2 expects separate params, not a URL; we’ll parse manually if needed.
    # For a standard URL like postgresql://user:pass@host:5432/dbname, psycopg2
    # can accept it directly via "dsn" parameter.
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
    """
    Main entry point used by the FastAPI route.

    If DATABASE_URL is set, use Postgres on AWS RDS.
    Otherwise, fall back to local DuckDB.
    """
    # Optional safety: only allow SELECT
    stripped = sql.strip().lower()
    if not stripped.startswith("select"):
        raise ValueError("Only SELECT queries are allowed in this demo")

    if DATABASE_URL:
        return _run_postgres(sql)
    else:
        return _run_duckdb(sql)
