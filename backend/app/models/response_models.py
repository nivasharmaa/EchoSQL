from pydantic import BaseModel
from typing import List, Any, Dict


class GenerateSQLResponse(BaseModel):
    sql: str
    warnings: List[str] = []


class RunSQLResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]


class SchemaColumn(BaseModel):
    name: str
    type: str


class SchemaTable(BaseModel):
    name: str
    columns: List[SchemaColumn]


class SchemaResponse(BaseModel):
    tables: List[SchemaTable]
