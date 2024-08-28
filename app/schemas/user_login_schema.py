from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    # email: EmailStr
    email: str
    password: str

class LoginResponseSchema(BaseModel):
    name: str
    # email: EmailStr
    email: str
    access_token: str
    role: str