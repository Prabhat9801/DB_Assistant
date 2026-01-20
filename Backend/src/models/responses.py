from pydantic import BaseModel
from typing import Any, List, Optional

class BaseResponseModel(BaseModel):
    success: bool
    message: Optional[str] = None

class DataResponseModel(BaseResponseModel):
    data: Any

class ListResponseModel(BaseResponseModel):
    data: List[Any]

class ErrorResponseModel(BaseResponseModel):
    error_code: str
    error_details: Optional[str] = None