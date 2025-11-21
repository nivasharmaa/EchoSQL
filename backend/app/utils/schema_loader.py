from textwrap import dedent


def load_demo_schema() -> str:
    return dedent("""
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
