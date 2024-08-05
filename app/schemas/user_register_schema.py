from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    class Config():
        # orm_mode = True
        from_attributes=True
