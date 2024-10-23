from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class ResponseSchema(BaseModel, Generic[T]):
    status: bool
    response: str
    data: Optional[T] = None

    class Config:
        from_attributes = True


# from pydantic import BaseModel
# from typing import Union, Optional

# class ResponseSchema(BaseModel):
#     status: bool = True
#     response: str
#     data: Union[Optional[dict], Optional[list], None] = None