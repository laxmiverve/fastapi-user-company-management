from pydantic import BaseModel

class UserCompanySchema(BaseModel):
    user_id: int
    company_id: int
    user_name: str
    user_email: str
    company_name: str
    company_email: str

    class Config:
        from_attributes = True
