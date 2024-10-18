from typing import Optional, List, Any

from pydantic import BaseModel, computed_field

class ListResponseModel(BaseModel):
    status: str
    details: List = []
    
class BoxFailureResponseModel(BaseModel):
    success: str
    message: str
    data: List = []