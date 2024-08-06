from pydantic import BaseModel

class CompanyResponseSchema(BaseModel):
    id: int
    company_name: str
    company_email: str
    company_number: str
    company_zipcode: str
    company_city: str
    company_state: str
    company_country: str

    # user_id: int

    class Config:
        from_attributes = True  