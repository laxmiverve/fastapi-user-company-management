from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserCompanyResponseSchema(BaseModel):
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
    # role_name: str
    companies: List[UserCompanyResponseSchema] 
    profile_img: Optional[str]

    class Config:
        from_attributes = True  


class CompanyDetailSchema(BaseModel):
    company_id: int
    company_name: str
    company_email: str

    class Config:
        from_attributes = True



class UserInformationSchema(BaseModel):
    user_id: int
    name: str
    email: str
    # password: str
    city: str
    state: str
    country: str
    role_id: int
    role_name: str  
    profile_img: Optional[str]
    # company: CompanyDetailSchema 
    company_details: Optional[CompanyDetailSchema] 

    class Config:
        from_attributes = True  