from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import generate_sql, run_sql, schema

app = FastAPI(title="Explain-Any-SQL API")

# CORS (we'll tighten origins later when frontend exists)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(generate_sql.router, prefix="/api", tags=["generate-sql"])
app.include_router(run_sql.router, prefix="/api", tags=["run-sql"])
app.include_router(schema.router, prefix="/api", tags=["schema"])
