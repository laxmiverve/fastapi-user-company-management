import base64
from typing import Optional
from fastapi import Header
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy.orm import Session, load_only, joinedload
from app.models.company_model import CompanyModel
from app.models.user_company_model import UserCompany
from app.models.user_model import UserModel
from app.schemas.company_response_schema import *
from app.schemas.company_update_schema import CompanyUpdateSchema
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid
from PIL import Image
from io import BytesIO


load_dotenv()

BASE_URL = os.getenv("BASE_URL")

# create a company
async def create_company(company_name: str, company_email: str, company_number: str, company_zipcode: Optional[str], company_city: Optional[str], company_state: Optional[str], company_country: Optional[str], company_profile: Optional[str], user_id: int, db: Session):
    try:
        existing_company = db.query(CompanyModel).filter(CompanyModel.company_email == company_email).first()

        if existing_company:
            return None
        
        new_company = CompanyModel(
            company_name=company_name,
            company_email=company_email,
            company_number=company_number,
            company_zipcode=company_zipcode,
            company_city=company_city,
            company_state=company_state,
            company_country=company_country,
            user_id=user_id,
            uuid=str(uuid.uuid4())
        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        company_profile_path = None
        if company_profile:
            if company_profile.startswith("data:"):
                header, company_profile = company_profile.split(",", 1)
            file_data = base64.b64decode(company_profile)
            image = Image.open(BytesIO(file_data))
            file_extension = f".{image.format.lower()}"
            
            timestamp = int(datetime.now().timestamp())
            company_profile_path = f"uploads/company/{new_company.id}_{timestamp}{file_extension}"

            with open(company_profile_path, "wb") as file:
                file.write(file_data)

            new_company.company_profile = company_profile_path
            db.commit()
            company_profile_url = f"{BASE_URL}{company_profile_path}"
        else:
            company_profile_url = None

        return CompanyResponseSchema(
            id=new_company.id,
            company_name=new_company.company_name,
            company_email=new_company.company_email,
            company_number=new_company.company_number,
            company_zipcode=new_company.company_zipcode,
            company_city=new_company.company_city,
            company_state=new_company.company_state,
            company_country=new_company.company_country,
            company_profile=company_profile_url,
            company_creator=new_company.company_creator,
            uuid=new_company.uuid,
        )
    except Exception as e:
        print("An exception occurred:", str(e))




# # get all company information
def get_all_company(db: Session, params: Params, sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    try:
        all_company = db.query(CompanyModel).options(load_only(CompanyModel.id, CompanyModel.company_email, CompanyModel.company_name, CompanyModel.company_city, CompanyModel.company_country, CompanyModel.company_state), joinedload(CompanyModel.company_creator).options(load_only(UserModel.name, UserModel.email, UserModel.country)))


        if sort_by and sort_direction:
            if sort_direction == "desc":
                all_company = all_company.order_by(getattr(CompanyModel, sort_by).desc())
            elif sort_direction == "asc":
                all_company = all_company.order_by(getattr(CompanyModel, sort_by).asc())
        
        paginated_company = paginate(all_company, params = params)

        for company in paginated_company.items:
            if company.company_profile:
                company.company_profile = f"{BASE_URL}{company.company_profile}"
        return paginated_company
    
    except Exception as e:
        print("An exception occurred:", str(e))




# get company by id
def get_company_by_id(company_id: int, db: Session):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            return None
        if company.company_profile:
                company.company_profile = f"{BASE_URL}{company.company_profile}"
        
        return company
    except Exception as e:
        print("An exception occurred:", str(e))




# delete company by id
def delete_company_by_id(company_id: int, db: Session):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()

        if company is None:
            return None
        
        if company.company_profile:
                company.company_profile = f"{BASE_URL}{company.company_profile}"

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
        return CompanyResponseSchema(
            id = existing_company.id,
            company_name = existing_company.company_name,
            company_email = existing_company.company_email,
            company_number = existing_company.company_number,
            company_zipcode = existing_company.company_zipcode,
            company_city = existing_company.company_city,
            company_state = existing_company.company_state,
            company_country = existing_company.company_country,
            company_profile = existing_company.company_profile,
            company_creator = existing_company.company_creator,
            uuid = existing_company.uuid
            )

        # return existing_company
    except Exception as e:
        print("Exception occurred:", str(e))


# add user to specific company
def add_user_to_company(company_id: int, user_id: int, db: Session):
    try:
        user_company = UserCompany(
            user_id = user_id,
            company_id = company_id
        )
        db.add(user_company)
        db.commit()
        db.refresh(user_company)
        return user_company
    
    except Exception as e:
        print("Exception occurred:", str(e))



# get all associated users of a specific company
def get_company_users(company_id: int, db: Session):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            return None

        users = db.query(UserModel).join(UserCompany).filter(UserCompany.company_id == company_id).all()

        user_details = [UserDetailSchema(user_id = user.id, user_name = user.name, user_email = user.email)
            for user in users
        ]

        company_with_users = CompanyWithUsersSchema(
            company_id = company.id,
            company_name = company.company_name,
            company_email = company.company_email,
            company_state = company.company_state,
            company_country = company.company_country,
            users = user_details
        )

        return company_with_users
    except Exception as e:
        print("Exception occurred:", str(e))




# get company information by using company id 
def get_company_details_by_id(company_id: int, db: Session):
    try:
        company = db.query(CompanyModel).options(joinedload(CompanyModel.company_creator)).filter(CompanyModel.id == company_id).first()
        
        if not company:
            return None
        
        created_by_user = company.company_creator

        def format_datetime(dt: datetime) -> str:
            return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None
        
        return CompanyDetailsSchema(
            company_id=company.id,
            company_name=company.company_name,
            description=company.company_profile,
            created_at=format_datetime(company.created_at),
            updated_at=format_datetime(company.updated_at),
            created_by_user={
                "user_id": created_by_user.id,
                "user_name": created_by_user.name,
                "user_email": created_by_user.email
            } 
        )
    except Exception as e:
        print("Exception occurred:", str(e))



    
# get company information by company uuid
def get_company_by_uuid(db: Session, uuid: str = Header(None)):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.uuid == uuid).one()
        company_profile_url = f"{BASE_URL}{company.company_profile}" if company.company_profile else None

        return CompanyResponseSchema(
            id = company.id,
            uuid = company.uuid,
            company_name = company.company_name,
            company_email = company.company_email,
            company_number = company.company_number,
            company_zipcode = company.company_zipcode,
            company_city = company.company_city,
            company_state = company.company_state,
            company_country = company.company_country,
            company_profile = company_profile_url,
            company_creator = company.company_creator
        )
    except Exception as e:
        print("An exception occurred:", str(e))
