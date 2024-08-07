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
    company_creator: CompanyCreatorSchema

    # user_id: int

    class Config:
        from_attributes = True  