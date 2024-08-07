from pydantic import BaseModel
from typing import Optional

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    new_password: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None