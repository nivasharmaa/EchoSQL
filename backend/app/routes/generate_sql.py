from fastapi import APIRouter, HTTPException

from app.models.request_models import GenerateSQLRequest
from app.models.response_models import GenerateSQLResponse
from app.services.llm_service import generate_sql_for_question
from app.utils.schema_loader import load_demo_schema

router = APIRouter(prefix="/sql", tags=["sql"])


@router.post("/generate", response_model=GenerateSQLResponse)
def generate_sql_endpoint(request: GenerateSQLRequest) -> GenerateSQLResponse:
    """
    Natural language -> SQL.
    """
    try:
        schema_ddl = load_demo_schema()  # load your demo schema
        sql = generate_sql_for_question(request.question, schema_ddl)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return GenerateSQLResponse(sql=sql, warnings=[])
