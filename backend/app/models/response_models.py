from pydantic import BaseModel
from typing import List, Any, Dict

class GenerateSQLResponse(BaseModel):
    sql: str
    explanation: str

class SchemaTable(BaseModel):
    name: str
    columns: List[str]

class SchemaResponse(BaseModel):
    tables: List[SchemaTable]

class RunSQLResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    # Later we can add: execution_time_ms, cost_estimate, warnings, etc.
