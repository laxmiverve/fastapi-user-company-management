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
        from_attributes = True
