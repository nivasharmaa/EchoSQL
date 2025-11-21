import os
from textwrap import dedent
from typing import Any, List, Tuple

import duckdb

# Simple file-based DuckDB for the demo
DB_PATH = os.getenv("DEMO_DB_PATH", "demo.duckdb")

SCHEMA_DDL = dedent("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE orders (
    id INTEGER,
    customer_id INTEGER,
    total_amount DOUBLE,
    status VARCHAR,
    created_at TIMESTAMP
);
""").strip()

SAMPLE_DATA_SQL = dedent("""
INSERT INTO customers (id, name, email, created_at) VALUES
  (1, 'Alice',   'alice@example.com',   '2024-01-10'),
  (2, 'Bob',     'bob@example.com',     '2024-02-05'),
  (3, 'Charlie', 'charlie@example.com', '2024-03-22');

INSERT INTO orders (id, customer_id, total_amount, status, created_at) VALUES
  (101, 1, 120.50, 'paid',      '2024-04-01'),
  (102, 1, 80.00,  'paid',      '2024-04-15'),
  (103, 2, 200.00, 'pending',   '2024-05-02'),
  (104, 3, 15.99,  'cancelled', '2024-05-03'),
  (105, 2, 55.75,  'paid',      '2024-06-01');
""").strip()


def init_demo_db() -> None:
    """Create demo schema + seed data (idempotent enough for dev)."""
    con = duckdb.connect(DB_PATH)
    try:
        con.execute(SCHEMA_DDL)
        # Clear existing rows so you don’t get duplicates on reload
        con.execute("DELETE FROM orders;")
        con.execute("DELETE FROM customers;")
        con.execute(SAMPLE_DATA_SQL)
    finally:
        con.close()


def run_select(sql: str) -> Tuple[List[str], List[List[Any]]]:
    """
    Run a SELECT query against the demo DB.

    - Only allows SELECT for safety.
    - Returns (columns, rows).
    """
    cleaned = sql.strip().rstrip(";")
    if not cleaned.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed in this demo.")

    con = duckdb.connect(DB_PATH)
    try:
        result = con.execute(cleaned)
        rows = result.fetchall()
        columns = [col[0] for col in result.description]  # [(name, ...), ...]
        return columns, rows
    finally:
        con.close()


# Initialize DB at import time (good enough for dev)
init_demo_db()
