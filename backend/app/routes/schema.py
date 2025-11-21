from fastapi import APIRouter

from app.models.response_models import (
    SchemaResponse,
    SchemaTable,
    SchemaColumn,
)

router = APIRouter(prefix="/schema", tags=["schema"])


@router.get("", response_model=SchemaResponse)
def get_schema() -> SchemaResponse:
    """
    Return a simple hardcoded schema that matches the demo DuckDB.
    """
    tables = [
        SchemaTable(
            name="customers",
            columns=[
                SchemaColumn(name="id", type="integer"),
                SchemaColumn(name="name", type="text"),
                SchemaColumn(name="email", type="text"),
                SchemaColumn(name="created_at", type="timestamp"),
            ],
        ),
        SchemaTable(
            name="orders",
            columns=[
                SchemaColumn(name="id", type="integer"),
                SchemaColumn(name="customer_id", type="integer"),
                SchemaColumn(name="total_amount", type="numeric"),
                SchemaColumn(name="status", type="text"),
                SchemaColumn(name="created_at", type="timestamp"),
            ],
        ),
    ]

    return SchemaResponse(tables=tables)
