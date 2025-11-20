from fastapi import APIRouter
from app.models.request_models import RunSQLRequest
from app.models.response_models import RunSQLResponse

router = APIRouter()

@router.post("/run-sql", response_model=RunSQLResponse)
async def run_sql_endpoint(payload: RunSQLRequest):
    # Temporary stub – DB integration comes next
    return RunSQLResponse(
        columns=["dummy_col"],
        rows=[[1]],
        row_count=1
    )
