import base64
from typing import Optional
from fastapi import Header, Request
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy.orm import Session, load_only, joinedload
from app.helper.email_sender import Helper
from app.models.company_model import CompanyModel
from app.models.roles_model import Role
from app.models.company_images import CompanyImage
from app.models.user_company_model import UserCompany
from app.models.user_model import UserModel
from app.schemas.company_register_schema import CompanyRegisterSchema
from app.schemas.company_response_schema import *
from app.schemas.company_update_schema import CompanyUpdateSchema
from app.schemas.user_company_schema import UserCompanySchema
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid
from PIL import Image
from io import BytesIO


load_dotenv()

BASE_URL = os.getenv("BASE_URL")

# create a new company
# async def create_company(company_data: CompanyRegisterSchema, request: Request, db: Session):
#     try:
#         user = Helper.getAuthUser(request, db)
#         if not user:
#             return None
        
#         if not Helper.is_valid_email(company_data.company_email):
#             return 1

#         # Ensure the user has the 'superadmin' role
#         role = db.query(Role).filter(Role.id == user.role_id).first()
#         if not role or role.id != 1:
#             return 2  # Not authorized to create company

#         existing_company = db.query(CompanyModel).filter(CompanyModel.company_email == company_data.company_email).first()
#         if existing_company:
#             return None  

#         new_company = CompanyModel(
#             company_name=company_data.company_name,
#             company_email=company_data.company_email,
#             company_number=company_data.company_number,
#             company_zipcode=company_data.company_zipcode,
#             company_city=company_data.company_city,
#             company_state=company_data.company_state,
#             company_country=company_data.company_country,
#             user_id=user.id,
#             uuid=str(uuid.uuid4())
#         )
#         db.add(new_company)
#         db.commit()
#         db.refresh(new_company)

#         company_images = []
#         company_profile_image = None

#         if company_data.company_profile:
#             image_data_list = company_data.company_profile.split("data:")

#             for index, image_data in enumerate(image_data_list):
#                 if image_data:
#                     if "," in image_data:
#                         header, image_data = image_data.split(",", 1)
#                     else:
#                         image_data = image_data.strip()

#                     file_data = base64.b64decode(image_data)
#                     image = Image.open(BytesIO(file_data))
#                     file_extension = f".{image.format.lower()}"
                    
#                     timestamp = int(datetime.now().timestamp())
#                     image_path = f"uploads/company/{new_company.id}_{timestamp}_{index}{file_extension}"
                    
#                     with open(image_path, "wb") as file:
#                         file.write(file_data)
                    
#                     company_images.append(image_path)

#                     if index == 1:
#                         company_profile_image = image_path

#         for image_path in company_images:
#             company_image = CompanyImage(
#                 image_path=image_path,
#                 company_id=new_company.id
#             )
#             db.add(company_image)
        
#         db.commit()

#         if company_profile_image:
#             new_company.company_profile = company_profile_image
#             db.commit()

#         company_profile_url = f"{BASE_URL}{company_profile_image}" if company_profile_image else None
#         company_images_urls = [f"{BASE_URL}{img}" for img in company_images]
#         response = {
#             "id": new_company.id,
#             "company_name": new_company.company_name,
#             "company_email": new_company.company_email,
#             "company_number": new_company.company_number,
#             "company_zipcode": new_company.company_zipcode,
#             "company_city": new_company.company_city,
#             "company_state": new_company.company_state,
#             "company_country": new_company.company_country,
#             "company_profile": company_profile_url,
#             "company_images": company_images_urls,
#             "company_creator": new_company.company_creator,
#             "uuid": new_company.uuid,
#         }
#         return response
#     except Exception as e:
#         print("An exception occurred:", str(e))



async def create_company(company_data: CompanyRegisterSchema, request: Request, db: Session):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return None
        
        if not Helper.is_valid_email(company_data.company_email):
            return 1

        # Ensure the user has the 'superadmin' role
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role or role.id != 1:
            return 2  # Not authorized to create company

        existing_company = db.query(CompanyModel).filter(CompanyModel.company_email == company_data.company_email).first()
        if existing_company:
            return None  

        new_company = CompanyModel(
            company_name = company_data.company_name,
            company_email = company_data.company_email,
            company_number = company_data.company_number,
            company_zipcode = company_data.company_zipcode,
            company_city = company_data.company_city,
            company_state = company_data.company_state,
            company_country = company_data.company_country,
            user_id = user.id,
            uuid=str(uuid.uuid4())
        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        company_images = []
        company_profile_image = None

        if company_data.company_profile:
            for index, image_data in enumerate(company_data.company_profile):
                if image_data:
                    if "," in image_data:
                        header, image_data = image_data.split(",", 1)
                    else:
                        image_data = image_data.strip()

                    file_data = base64.b64decode(image_data)
                    image = Image.open(BytesIO(file_data))
                    file_extension = f".{image.format.lower()}"
                    
                    image_number = index + 1
                    timestamp = int(datetime.now().timestamp())
                    image_path = f"uploads/company/{new_company.id}_{timestamp}_{image_number}{file_extension}"
                    
                    with open(image_path, "wb") as file:
                        file.write(file_data)
                    
                    company_images.append(image_path)

                    if index == 0:  
                        company_profile_image = image_path

        for image_path in company_images:
            company_image = CompanyImage(
                image_path = image_path,
                company_id = new_company.id
            )
            db.add(company_image)
        
        db.commit()

        if company_profile_image:
            new_company.company_profile = company_profile_image
            db.commit()

        company_profile_url = f"{BASE_URL}{company_profile_image}" if company_profile_image else None
        company_images_urls = [f"{BASE_URL}{img}" for img in company_images]

        response = {
            "id": new_company.id,
            "company_name": new_company.company_name,
            "company_email": new_company.company_email,
            "company_number": new_company.company_number,
            "company_zipcode": new_company.company_zipcode,
            "company_city": new_company.company_city,
            "company_state": new_company.company_state,
            "company_country": new_company.company_country,
            "company_profile": company_profile_url,
            "company_images": company_images_urls,  
            "company_creator": new_company.company_creator,
            "uuid": new_company.uuid,
        }
        return response
    except Exception as e:
        print("An exception occurred:", str(e))



# get all company information
def get_all_company(request: Request, db: Session, params: Params, sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return None

        # Ensure the user has role_id 1 (superadmin) to allow company list view
        if user.role_id != 1:
            return 1  # Not authorized to view companies
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
def get_company_by_id(company_id: int, request: Request, db: Session):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return None

        # Check if the user has role_id 1 (superadmin) or role_id 2 (companyadmin)
        if user.role_id != 1 and user.role_id != 2:
            return 1  # Not authorized to view the company
    
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            return None
        if company.company_profile:
                company.company_profile = f"{BASE_URL}{company.company_profile}"
        
        return company
    except Exception as e:
        print("An exception occurred:", str(e))




# delete company by id
def delete_company_by_id(company_id: int, request: Request, db: Session):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return None

        # Check if the user has role_id 1 (superadmin) to allow deletion
        if user.role_id != 1:
            return 1  # Not authorized to delete the company
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
def update_company_by_id(company_id: int,  request: Request, db: Session, company_data: CompanyUpdateSchema):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return None

        # Check if the user has role_id 1 (superadmin) to allow updates
        if user.role_id != 1:
            return 1  # Not authorized to update the company
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

    except Exception as e:
        print("Exception occurred:", str(e))


# add user to specific company
def add_user_to_company(company_id: int, request: Request, user_id: int, db: Session):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return 1 # User not found

        if user.role_id != 2:
            return 2  # Not authorized
        
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            return 3  # Company not found
        
        user_to_add = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_to_add:
            return 4  # User to add not found
        
        existing_user_company = db.query(UserCompany).filter_by(user_id=user_id, company_id=company_id).first()
        if existing_user_company:
            return 5  # User already in the company
        
        user_association = db.query(UserCompany).filter_by(user_id=user_id).first()
        if user_association:
            user_associated_company = db.query(CompanyModel).filter(CompanyModel.id == user_association.company_id).first()
            return 6  # User in another company
        
        user_company = UserCompany(user_id=user_id, company_id=company_id)
        db.add(user_company)
        db.commit()
        db.refresh(user_company)
        
        return UserCompanySchema(
            user_id = user_company.user_id,
            company_id = user_company.company_id,
            user_name = user_to_add.name,
            user_email = user_to_add.email,
            company_name = company.company_name,
            company_email = company.company_email
        )

    except Exception as e:
        print("Exception occurred:", str(e))



def get_company_users(company_id: int, request: Request, db: Session):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return None
            # return 2  # User not found

        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            return 1  # Company not found

        # Check if the user has role_id 1 (superadmin) or role_id 2 (companyadmin)
        if user.role_id != 1 and user.role_id != 2:
            return 2  # Not authorized to view the company

        users = db.query(UserModel).join(UserCompany).filter(UserCompany.company_id == company_id).all()

        user_details = [UserDetailSchema(user_id=user.id, user_name=user.name, user_email=user.email)
                        for user in users]

        company_with_users = CompanyWithUsersSchema(
            company_id = company.id,
            company_name = company.company_name,
            company_email = company.company_email,
            company_state = company.company_state,
            company_country = company.company_country,
            users = user_details
        )

        if not company_with_users.users:
            return 3  # No users found

        return company_with_users
    except Exception as e:
        print("Exception occurred:", str(e))




# get created and updated time of the company
def get_company_details_by_id(company_id: int, request: Request,  db: Session):
    try:
        user = Helper.getAuthUser(request, db)
        if not user:
            return None

        # access is only granted if the user has either role ID 1 or 2
        if user.role_id != 1 and user.role_id != 2:
            return 1
        
        company = db.query(CompanyModel).options(joinedload(CompanyModel.company_creator)).filter(CompanyModel.id == company_id).first()
        
        if not company:
            return None
        
        created_by_user = company.company_creator

        def format_datetime(dt: datetime) -> str:
            return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None
        
        return CompanyDetailsSchema(
            company_id = company.id,
            company_name = company.company_name,
            description = company.company_profile,
            created_at = format_datetime(company.created_at),
            updated_at = format_datetime(company.updated_at),
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
        company_images = [f"{BASE_URL}{img.image_path}" for img in company.images] if company.images else None

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
            company_images=company_images,
            company_creator = company.company_creator
        )
    except Exception as e:
        print("An exception occurred:", str(e))
