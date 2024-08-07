from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class LoginResponseSchema(BaseModel):
    name: str
    email: EmailStr
    access_token: str
    role: str