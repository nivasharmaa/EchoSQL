import os
from textwrap import dedent

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = dedent("""
You are a senior data engineer.
Given: (1) a database schema (DDL) and (2) a natural language question,
produce a single, syntactically-correct SQL query for PostgreSQL.

Rules:
- ONLY return the SQL. No explanations.
- Prefer SELECT queries.
- NEVER modify, drop, or truncate tables.
- If the question is ambiguous, make a reasonable assumption and proceed.
""").strip()


def build_prompt(question: str, schema_ddl: str) -> str:
    return dedent(f"""
    Database schema (DDL):
    {schema_ddl}

    Question:
    {question}

    Task:
    Write a single PostgreSQL SQL query that answers the question.
    Return ONLY the SQL.
    """).strip()


def clean_sql(raw: str) -> str:
    """
    Remove ```sql ... ``` wrappers if model adds them.
    """
    raw = raw.strip()
    if raw.startswith("```"):
        # strip first fence
        lines = raw.splitlines()
        # drop first line
        lines = lines[1:]
        # drop closing fence if present
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    return raw


def generate_sql_for_question(question: str, schema_ddl: str) -> str:
    prompt = build_prompt(question, schema_ddl)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # cheap + good enough for MVP
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    raw = response.choices[0].message.content or ""
    sql = clean_sql(raw)

    return sql
