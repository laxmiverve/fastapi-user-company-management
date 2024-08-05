from pydantic import BaseModel, EmailStr

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    city: str
    state: str
    country: str

    class Config:
        from_attributes = True  