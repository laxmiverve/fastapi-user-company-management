from typing import List, Optional
from pydantic import BaseModel, EmailStr

# company details of a specific user
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
    companies: List[UserCompanyResponseSchema] 
    profile_img: Optional[str]

    class Config:
        from_attributes = True  

# get company details
class CompanyDetailSchema(BaseModel):
    company_id: int
    company_name: str
    company_email: str

    class Config:
        from_attributes = True


# get all user info
class UserInformationSchema(BaseModel):
    user_id: int
    name: str
    email: str
    city: str
    state: str
    country: str
    role_id: int
    role_name: str  
    profile_img: Optional[str]
    company_details: Optional[CompanyDetailSchema] 

    class Config:
        from_attributes = True  