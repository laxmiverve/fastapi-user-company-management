from pydantic import BaseModel
from typing import Optional

class CompanyUpdateSchema(BaseModel):
    company_name: Optional[str] = None
    company_email: Optional[str] = None
    company_number: Optional[str] = None
    company_zipcode: Optional[str] = None
    company_city: Optional[str] = None
    company_state: Optional[str] = None
    company_country: Optional[str] = None