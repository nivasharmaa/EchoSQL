from fastapi import APIRouter, HTTPException

from app.models.request_models import RunSQLRequest
from app.models.response_models import RunSQLResponse
from app.services.db_service import run_query

router = APIRouter(tags=["run-sql"])


@router.post("/run-sql", response_model=RunSQLResponse)
def run_sql_endpoint(request: RunSQLRequest) -> RunSQLResponse:
    """
    Execute a read-only SQL query against the configured database.
    """
    try:
        columns, rows = run_query(request.sql)
        return RunSQLResponse(columns=columns, rows=rows)
    except Exception as e:
        # You can log e here if you want
        raise HTTPException(status_code=500, detail=str(e))
