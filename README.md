# EchoSQL (Prototype)

Explain-Any-SQL is a full-stack prototype that translates natural language questions into SQL, executes the generated query on a live database, and returns the results through a clean web interface. The project demonstrates end-to-end integration across backend APIs, database execution, and an LLM-based SQL generation layer.

This prototype is built with FastAPI, Next.js, DuckDB (with Postgres/RDS support), and the OpenAI API.

---

## Overview

The system allows users to enter natural language questions such as:

“List all customers who have placed more than 3 orders.”

The backend generates SQL based on the question and the known database schema. It then safely executes the SQL against a demo database and returns the results to the frontend.

The workflow:

1. Natural language input
2. SQL generation (LLM)
3. Validation (SELECT-only)
4. Database execution
5. Display results in the UI

---

## Features

* Natural language to SQL translation using GPT-4.1-mini
* SQL validation to prevent non-SELECT operations
* Real query execution using DuckDB (default)
* Optional Postgres/AWS RDS support via a single environment variable
* FastAPI backend with typed request/response models
* Next.js frontend with loading states, error handling, and table rendering
* Schema-aware SQL generation using a DDL view of the database

---

## Tech Stack

**Backend:** FastAPI, Python, DuckDB, Pydantic, OpenAI API
**Frontend:** Next.js 14 (App Router), React, TypeScript, Tailwind
**Database:** DuckDB (demo), Postgres/RDS compatible

---

## Project Structure

```
explain-any-sql/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   └── utils/
│   └── requirements.txt
│
└── frontend/
    ├── app/
    ├── public/
    └── package.json
```

---

## How to Run

### Backend

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

### Frontend

```
cd frontend
npm install
npm run dev
```

Open: [http://localhost:3000](http://localhost:3000)

---

## Environment Variables

Create a `.env` file in the `backend` directory:

```
OPENAI_API_KEY=your_key_here
DB_PATH=demo.db
DATABASE_URL=postgresql://user:password@host:5432/dbname   # optional
```

If `DATABASE_URL` is set, the backend will use Postgres/RDS.
If not, it defaults to a local DuckDB database with seeded demo data.

---

## Demo Queries (Examples)

The following queries work well with the seeded demo database:

* “How many customers are in the database?”
* “Show all orders with a total amount greater than 100.”
* “List each customer with their total order amount.”
* “List all customers who have placed more than 3 orders.”

---

## Database

By default, the system uses DuckDB and automatically initializes:

Tables:

* `customers`
* `orders`

It also seeds sample rows for testing and demonstrations.

To switch to Postgres or AWS RDS, set `DATABASE_URL` and restart the backend.

---

## Notes

This prototype is intended for demonstration purposes.
The design emphasizes correctness, clarity, and portability between different database engines.
The architecture supports further extension, including schema ingestion, query explanations, authentication, and production database connections.


