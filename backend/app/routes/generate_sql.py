from fastapi import APIRouter
from app.models.request_models import GenerateSQLRequest
from app.models.response_models import GenerateSQLResponse

router = APIRouter()

@router.post("/generate-sql", response_model=GenerateSQLResponse)
async def generate_sql_endpoint(payload: GenerateSQLRequest):
    # Temporary stub – will plug in LLM later
    return GenerateSQLResponse(
        sql="SELECT 1;",
        explanation="Stub response – replace with LLM generated SQL."
    )
