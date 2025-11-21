from fastapi import APIRouter, HTTPException

from app.models.request_models import RunSQLRequest
from app.models.response_models import RunSQLResponse
from app.services.db_service import run_select

router = APIRouter(prefix="/run-sql", tags=["run-sql"])


@router.post("", response_model=RunSQLResponse)
def run_sql_endpoint(request: RunSQLRequest) -> RunSQLResponse:
    """
    Execute a SELECT query against the demo DuckDB instance.
    """
    try:
        columns, rows = run_select(request.sql)
    except ValueError as e:
        # e.g., non-SELECT queries
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    return RunSQLResponse(columns=columns, rows=rows)
