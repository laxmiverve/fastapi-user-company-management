from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class ResponseSchema(BaseModel, Generic[T]):
    status: bool
    response: str
    data: Optional[T] = None

    class Config:
        from_attributes = True
