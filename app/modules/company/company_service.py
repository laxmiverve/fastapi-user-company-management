from typing import Optional
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy.orm import Session, load_only, joinedload
from app.models.company_model import CompanyModel
from app.models.user_model import UserModel
from app.schemas.company_register_schema import CompanyRegisterSchema
from app.schemas.company_update_schema import CompanyUpdateSchema
from datetime import datetime




# create a new company
def create_company(company: CompanyRegisterSchema, user_id: int, db: Session):
    try:
        existing_company = db.query(CompanyModel).filter(CompanyModel.company_email == company.company_email).first()

        if existing_company:
            return None

        new_company = CompanyModel(
            company_name = company.company_name,
            company_email = company.company_email,
            company_number = company.company_number,
            company_zipcode = company.company_zipcode,
            company_city = company.company_city,
            company_state = company.company_state,
            company_country = company.company_country,
            user_id = user_id,
            created_at=datetime.now()
        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        return new_company
    except Exception as e:
        print("Exception occurred", str(e))




# get all company information
def get_all_company(db: Session, params: Params, sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    try:
        all_company = db.query(CompanyModel).options(load_only(CompanyModel.id, CompanyModel.company_email, CompanyModel.company_name, CompanyModel.company_city, CompanyModel.company_country, CompanyModel.company_state), joinedload(CompanyModel.company_creator).options(load_only(UserModel.name, UserModel.email, UserModel.country)))


        if sort_by and sort_direction:
            if sort_direction == "desc":
                all_company = all_company.order_by(getattr(CompanyModel, sort_by).desc())
            elif sort_direction == "asc":
                all_company = all_company.order_by(getattr(CompanyModel, sort_by).asc())
        
        paginated_company = paginate(all_company, params = params)
        return paginated_company
    
    except Exception as e:
        print("An exception occurred:", str(e))



# get company by id
def get_company_by_id(company_id: int, db: Session):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            return None
        
        return company
    except Exception as e:
        print("An exception occurred:", str(e))



# delete company by id
def delete_company_by_id(company_id: int, db: Session):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()

        if company is None:
            return None

        db.delete(company)
        db.commit()

        return company

    except Exception as e:
        print("Exception occurred:", str(e))




# update company by id 
def update_company_by_id(company_id: int, db: Session, company_data: CompanyUpdateSchema):
    try:
        existing_company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()

        if not existing_company:
            return None

        if company_data.company_name is not None:
            existing_company.company_name = company_data.company_name

        if company_data.company_email is not None:
            existing_company.company_email = company_data.company_email

        if company_data.company_number is not None:
            existing_company.company_number = company_data.company_number

        if company_data.company_zipcode is not None:
            existing_company.company_zipcode = company_data.company_zipcode

        if company_data.company_city is not None:
            existing_company.company_city = company_data.company_city

        if company_data.company_state is not None:
            existing_company.company_state = company_data.company_state

        if company_data.company_country is not None:
            existing_company.company_country = company_data.company_country
        
        existing_company.updated_at = datetime.now()

        db.commit()
        db.refresh(existing_company)

        return existing_company
    except Exception as e:
        print("Exception occurred:", str(e))

