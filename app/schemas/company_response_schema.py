from typing import List, Optional
from pydantic import BaseModel

class CompanyCreatorSchema(BaseModel):
    name: str
    email: str
    country: str

    class Config:
        from_attributes = True


class CompanyResponseSchema(BaseModel):
    id: int
    company_name: str
    company_email: str
    company_number: str
    company_zipcode: str
    company_city: str
    company_state: str
    company_country: str
    company_profile: Optional[str]
    company_creator: CompanyCreatorSchema

    class Config:
        from_attributes = True  


class UserDetailSchema(BaseModel):
    user_id: int
    user_name: str
    user_email: str

    class Config:
        from_attributes = True


class CompanyWithUsersSchema(BaseModel):
    company_id: int
    company_name: str
    company_email: str
    company_state: str
    company_country: str
    users: List[UserDetailSchema]

    class Config:
        from_attributes = True


class CompanyDetailsSchema(BaseModel):
    company_id: int
    company_name: str
    created_at: Optional[str]
    updated_at: Optional[str]  
    created_by_user: Optional[UserDetailSchema] = None