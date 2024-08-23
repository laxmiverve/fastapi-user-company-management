from pydantic import BaseModel
from typing import Optional

class CompanyRegisterSchema(BaseModel):
    company_name: str
    company_email: str
    company_number: str
    company_zipcode: Optional[str] = None
    company_city: Optional[str] = None
    company_state: Optional[str] = None
    company_country: Optional[str] = None
    company_profile: Optional[str] = None

    class Config():
        from_attributes = True

