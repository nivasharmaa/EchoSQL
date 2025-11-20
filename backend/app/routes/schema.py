from fastapi import APIRouter
from app.models.response_models import SchemaResponse

router = APIRouter()

@router.get("/schema", response_model=SchemaResponse)
async def get_schema():
    # Stub – will be wired to db_service later
    return SchemaResponse(tables=[])
