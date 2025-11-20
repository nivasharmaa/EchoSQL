from pydantic import BaseModel

class GenerateSQLRequest(BaseModel):
    question: str

class RunSQLRequest(BaseModel):
    sql: str
