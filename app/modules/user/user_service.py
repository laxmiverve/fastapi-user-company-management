from datetime import datetime
from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import or_
from fastapi_pagination import Params
from app.models.user_model import UserModel
from app.models.company_model import CompanyModel
from app.schemas.user_register_schema import UserRegisterSchema
from app.schemas.user_update_schema import UserUpdateSchema
from app.hashing.password_hash import Hash
from app.helper.email_sender import Helper
from app.auth.jwt_handler import decode_jwt_token
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Optional

# New user register
def create_user(user_data: UserRegisterSchema, profile_img_filename: Optional[str], background_tasks: BackgroundTasks, db: Session):
    try:
        existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

        if existing_user:
            return None

        new_user = UserModel(
            name = user_data.name,
            email = user_data.email,
            password = Hash.bcrypt(user_data.password),
            city = user_data.city,
            state = user_data.state,
            country = user_data.country,
            role_id = user_data.role_id,
            profile_img = profile_img_filename, 
            created_at = datetime.now() 
        )

        def send_email_task():
            Helper.regd_mail_send(user_data.email)

        background_tasks.add_task(send_email_task)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    except Exception as e:
        print("Exception occurred:", str(e))



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

        paginated_users = paginate(all_user, params = params)
        return paginated_users
    
    except Exception as e:
        print("Exception occurred:", str(e))




# Get user information by id
def show_user(id: int, db: Session):
    try:
        user = db.query(UserModel).options(load_only(UserModel.id, UserModel.name, UserModel.email, UserModel.city, UserModel.state, UserModel.country)).filter(UserModel.id == id).first()

        if not user:
            return None

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

        return user
    
    except Exception as e:
        print("Exception occurred:", str(e))



# Delete user by id
def delete_user_info(id: int, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.id == id).first()

        if user is None:
            return None

        db.delete(user)
        db.commit()

        return user
    
    except Exception as e:
        print("Exception occurred:", str(e))
