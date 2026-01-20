from pydantic import BaseModel
from typing import Optional, List

class DynamicRequestModel(BaseModel):
    """Base model for dynamic requests."""
    table: str
    columns: List[str]
    filters: Optional[dict] = None

class CreateRecordRequest(BaseModel):
    """Request model for creating a new record."""
    table: str
    data: dict

class UpdateRecordRequest(BaseModel):
    """Request model for updating an existing record."""
    table: str
    data: dict
    filters: dict

class DeleteRecordRequest(BaseModel):
    """Request model for deleting a record."""
    table: str
    filters: dict

class QueryRequest(BaseModel):
    """Request model for executing a custom query."""
    query: str