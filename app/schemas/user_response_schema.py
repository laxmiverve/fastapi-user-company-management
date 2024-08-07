from typing import List
from pydantic import BaseModel, EmailStr


class UserCompanySchema(BaseModel):
    company_name: str
    company_email: str
    company_country: str

    class Config:
        from_attributes = True  

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    city: str
    state: str
    country: str
    # companies: UserCompanySchema
    companies: List[UserCompanySchema] 

    class Config:
        from_attributes = True  