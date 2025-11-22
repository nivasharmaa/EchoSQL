import os
from typing import List, Tuple, Any

import duckdb

# Use a local DuckDB file; you can change the path if you want
DB_PATH = os.getenv("DB_PATH", "demo.db")


def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Return a DuckDB connection to the local demo database file.
    """
    return duckdb.connect(DB_PATH)


def init_demo_db() -> None:
    """
    Create demo tables + seed some data if they don't exist / are empty.
    This is just for the MVP demo.
    """
    conn = get_connection()
    try:
        # Customers table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id          INTEGER,
                name        TEXT,
                email       TEXT,
                created_at  TIMESTAMP
            );
            """
        )

        # Orders table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id           INTEGER,
                customer_id  INTEGER,
                total_amount DOUBLE,
                created_at   TIMESTAMP
            );
            """
        )

        # Seed data only if empty
        customers_count = conn.execute("SELECT COUNT(*) FROM customers;").fetchone()[0]
        orders_count = conn.execute("SELECT COUNT(*) FROM orders;").fetchone()[0]

        if customers_count == 0 and orders_count == 0:
            conn.execute(
                """
                INSERT INTO customers (id, name, email, created_at) VALUES
                    (1, 'Alice',   'alice@example.com',   '2024-01-01'),
                    (2, 'Bob',     'bob@example.com',     '2024-02-01'),
                    (3, 'Charlie', 'charlie@example.com', '2024-03-01'),
                    (4, 'Diana',   'diana@example.com',   '2024-04-01');
                """
            )

            # Make sure at least one customer has > 3 orders for your demo query
            conn.execute(
                """
                INSERT INTO orders (id, customer_id, total_amount, created_at) VALUES
                    (101, 1, 120.50, '2024-05-01'),
                    (102, 1,  80.00, '2024-05-10'),
                    (103, 1, 200.00, '2024-05-15'),
                    (104, 1,  50.00, '2024-05-20'),
                    (201, 2,  75.00, '2024-06-01'),
                    (202, 2,  40.00, '2024-06-05'),
                    (301, 3, 300.00, '2024-07-01');
                """
            )
    finally:
        conn.close()


def run_select(sql: str) -> Tuple[List[str], List[List[Any]]]:
    """
    Run a SELECT-only query against the demo DB and return (columns, rows).

    - Raises ValueError if the query is not a SELECT.
    """
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        raise ValueError("Only SELECT queries are allowed in this demo.")

    conn = get_connection()
    try:
        result = conn.execute(sql)
        # DuckDB cursor-style description: list of (name, type, ...)
        description = result.description
        columns = [col[0] for col in description]
        rows = result.fetchall()  # List[List[Any]]
        return columns, rows
    finally:
        conn.close()


# Initialize demo DB on import
init_demo_db()
