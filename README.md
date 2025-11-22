# EchoSQL (Prototype)

This project is a working prototype that converts natural language questions into SQL and executes the generated SQL on a demo database. The system includes a FastAPI backend, a Next.js frontend, and an LLM-powered SQL generation layer using the OpenAI API. The goal of this prototype is to demonstrate an end-to-end workflow for natural language → SQL → query results.

---

## Demo Video
Watch the walkthrough here: https://drive.google.com/file/d/13o7EDJCYjVDZC74IIQJ7qKOakiMReH3i/view?usp=sharing

---

## Features Implemented

* Natural language to SQL generation using the OpenAI GPT-4.1-mini API
* SQL cleaning and validation (SELECT-only)
* Execution of SQL queries against a local DuckDB database
* Pre-seeded demo tables (`customers`, `orders`) for predictable outputs
* FastAPI backend with three endpoints:

  * `/api/sql/generate`
  * `/api/run-sql`
  * `/api/schema`
* Next.js frontend to:

  * Enter a question
  * View generated SQL
  * Execute SQL
  * Display query results in a table
  * Show loading states and error messages

Everything shown in this README is built and functioning in the final prototype.

---

## Tech Stack Used

**Backend:**

* Python
* FastAPI
* DuckDB
* Pydantic
* Uvicorn

**Frontend:**

* Next.js (App Router)
* React
* TypeScript
* TailwindCSS

**AI:**

* OpenAI GPT-4.1-mini (Chat Completions)

---

## Project Structure (Actual)

```
backend/
  app/
    main.py
    routes/
      generate_sql.py
      run_sql.py
      schema.py
    services/
      llm_service.py
      db_service.py
    models/
      request_models.py
      response_models.py
    utils/
      schema_loader.py
  requirements.txt

frontend/
  app/
    page.tsx
  package.json
  tailwind.config.js
```

---

## Running the Backend

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

### Backend Environment Variables

Create a `.env` file inside `backend`:

```
OPENAI_API_KEY=your_key_here
DB_PATH=demo.db
```

DuckDB is used automatically.
A demo database is created and seeded on startup.

---

## Running the Frontend

```
cd frontend
npm install
npm run dev
```

Open the app at:

```
http://localhost:3000
```

---

## What This Prototype Demonstrates

* LLM prompting and SQL generation
* Backend–frontend integration
* Database querying and safe execution
* Modern full-stack structure (FastAPI + Next.js)
* Real working NL → SQL → results pipeline

---

## Upcoming Enhancements

* AWS RDS PostgreSQL support for production-grade, cloud-hosted database execution
* Environment-aware routing between local DuckDB and RDS
* Improved schema sync and validation for enterprise deployments

