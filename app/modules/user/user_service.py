from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy.orm import Session, load_only, joinedload
from app.auth.jwt_handler import decode_jwt_token
from app.hashing.password_hash import Hash
from app.models.company_model import CompanyModel
from app.models.roles_model import Role
from app.models.user_model import UserModel
from app.schemas.user_register_schema import UserRegisterSchema
from app.schemas.user_update_schema import UserUpdateSchema

# New user register
def create_user(user_data: UserRegisterSchema, db: Session):
    try:
        existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

        if existing_user:
            return None
        
        # role = db.query(Role).filter(Role.id == user_data.role_id).first()
        # if not role:
        #     return {"message" : "Invalid role id"}
        
        new_user = UserModel(
            name = user_data.name,
            email = user_data.email,
            password = Hash.bcrypt(user_data.password),
            city = user_data.city,
            state = user_data.state,
            country = user_data.country,
            role_id=user_data.role_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as e:
        print("Exception occurred:", str(e))





# Get all user information
def get_all_users(db: Session, params: Params, sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    try:
        query = db.query(UserModel).options(load_only(UserModel.email, UserModel.name, UserModel.city, UserModel.country, UserModel.state), joinedload(UserModel.companies).load_only(CompanyModel.id, CompanyModel.company_name, CompanyModel.company_email, CompanyModel.company_country))

        if sort_by and sort_direction:
            if sort_direction == "desc":
                query = query.order_by(getattr(UserModel, sort_by).desc())
            elif sort_direction == "asc":
                query = query.order_by(getattr(UserModel, sort_by).asc())

        paginated_users = paginate(query, params = params)
        return paginated_users
    except Exception as e:
        print("An exception occurred:", str(e))



# Get user information by id
def show_user(id: int, db: Session):
    try:
        user = db.query(UserModel).options(load_only(UserModel.id, UserModel.name, UserModel.email, UserModel.city, UserModel.state, UserModel.country)).filter(UserModel.id == id).first()
        
        if not user:
            return None
        
        return user    
    except Exception as e:
        print("An exception occurred:", str(e))




# Update current logged user
def update_user_info(user_update_data: UserUpdateSchema, token: str, db: Session):
    try:
        user_email = decode_jwt_token(token)
        user = db.query(UserModel).filter(UserModel.email == user_email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user_update_data.name is not None:
            user.name = user_update_data.name

        if user_update_data.new_password is not None:
            if Hash.verify(user.password, user_update_data.new_password):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "New password must be different from the current password")
            
            user.password = Hash.bcrypt(user_update_data.new_password)

        # if user_update_data.email is not None:
        #     user.email = user_update_data.email

        if user_update_data.city is not None:
            user.city = user_update_data.city

        if user_update_data.state is not None:
            user.state = user_update_data.state

        if user_update_data.country is not None:
            user.country = user_update_data.country

        db.commit()

        return user

    except Exception as e:
        print("An exception occurred:", str(e))






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
