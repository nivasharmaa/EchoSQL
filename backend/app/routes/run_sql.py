from fastapi import APIRouter, HTTPException

from app.models.request_models import RunSQLRequest
from app.models.response_models import RunSQLResponse
from app.services.db_service import run_query

router = APIRouter(prefix="/run-sql", tags=["run-sql"])

@router.post("", response_model=RunSQLResponse)
def run_sql_endpoint(request: RunSQLRequest) -> RunSQLResponse:
    try:
        columns, rows = run_query(request.sql)
        return RunSQLResponse(columns=columns, rows=rows)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
