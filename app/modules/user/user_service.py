from datetime import datetime
import pathlib
from fastapi import BackgroundTasks, HTTPException, UploadFile, status
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import or_
from fastapi_pagination import Params
from app.models.roles_model import Role
from app.models.user_model import UserModel
from app.models.company_model import CompanyModel
from app.schemas.user_response_schema import UserResponseSchema
from app.schemas.user_update_schema import UserUpdateSchema
from app.hashing.password_hash import Hash
from app.auth.jwt_handler import decode_jwt_token
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Optional
import os
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("BASE_URL")


# New user register
async def create_user(name: str, email: str, password: str, role_id: int, city: str, state: str, country: str, profile_img: Optional[UploadFile], background_tasks: BackgroundTasks, db: Session):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
        
        existing_user = db.query(UserModel).filter(UserModel.email == email).first()
        if existing_user:
            return None

        new_user = UserModel( 
            name = name,
            email = email,
            password = Hash.bcrypt(password),
            role_id = role_id,
            city = city,
            state = state,
            country = country,
            # profile_img = profile_img_path,
            created_at = datetime.now()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        profile_img_path = None
        if profile_img:
            filename = profile_img.filename
            timestamp = int(datetime.now().timestamp())
            file_extension = pathlib.Path(filename).suffix

            profile_img_path = f"uploads/user/{new_user.id}_{timestamp}{file_extension}"
            contents = await profile_img.read()

            with open(profile_img_path, "wb") as f:
                f.write(contents)
            
            new_user.profile_img = profile_img_path
            db.commit()

        user_profile_url = f"{BASE_URL}{profile_img_path}" if profile_img_path else None

        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "city": new_user.city,
            "state": new_user.state,
            "country": new_user.country,
            "profile_img": user_profile_url,
            "companies": []  
        }
    except Exception as e:
        print("Exception occurred", str(e))



# Get all user information
def get_all_users(db: Session, params: Params, search_string: str, sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    try:
        all_user = db.query(UserModel).options(load_only(UserModel.email, UserModel.name, UserModel.city, UserModel.country, UserModel.state), joinedload(UserModel.companies).load_only(CompanyModel.id, CompanyModel.company_name, CompanyModel.company_email, CompanyModel.company_country))

        if sort_by and sort_direction:
            if sort_direction == "desc":
                all_user = all_user.order_by(getattr(UserModel, sort_by).desc())
            elif sort_direction == "asc":
                all_user = all_user.order_by(getattr(UserModel, sort_by).asc())

        if search_string:
            all_user = all_user.filter(or_(
                UserModel.name.like('%' + search_string + '%'),
                UserModel.email.like('%' + search_string + '%')
            ))

        paginated_users = paginate(all_user, params=params)
        
        for user in paginated_users.items:
            if user.profile_img:
                user.profile_img = f"{BASE_URL}{user.profile_img}"
        
        return paginated_users

    except Exception as e:
        print("Exception occurred:", str(e))
        return None




# Get user information by id
def show_user(id: int, db: Session):
    try:
        user = db.query(UserModel).options(load_only(UserModel.id, UserModel.name, UserModel.email, UserModel.city, UserModel.state, UserModel.country, UserModel.profile_img)).filter(UserModel.id == id).first()

        if not user:
            return None

        if user.profile_img:
            user.profile_img = f"{BASE_URL}{user.profile_img}"
        
        return user
    except Exception as e:
        print("Exception occurred:", str(e))




# Update current logged user
def update_user_info(user_update_data: UserUpdateSchema, token: str, db: Session):
    try:
        user_email = decode_jwt_token(token)
        user = db.query(UserModel).filter(UserModel.email == user_email).first()

        if not user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")

        if user_update_data.name is not None:
            user.name = user_update_data.name

        if user_update_data.new_password is not None:
            if Hash.verify(user.password, user_update_data.new_password):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "New password must be different from the current password")

            user.password = Hash.bcrypt(user_update_data.new_password)

        if user_update_data.city is not None:
            user.city = user_update_data.city

        if user_update_data.state is not None:
            user.state = user_update_data.state

        if user_update_data.country is not None:
            user.country = user_update_data.country

        user.updated_at = datetime.now() 
        db.commit()
        return UserResponseSchema(
            id = user.id,
            name = user.name,
            email = user.email,
            city = user.city,
            state = user.state,
            country = user.country,
            companies = [], 
            profile_img = user.profile_img
        )
        # return user
    
    except Exception as e:
        print("Exception occurred:", str(e))



# Delete user by id
def delete_user_info(id: int, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.id == id).first()

        if user is None:
            return None
        
        if user.profile_img:
            user.profile_img = f"{BASE_URL}{user.profile_img}"

        db.delete(user)
        db.commit()

        return user
    
    except Exception as e:
        print("Exception occurred:", str(e))
