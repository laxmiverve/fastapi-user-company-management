# from typing import Optional
# from fastapi import Depends, Form, HTTPException, status
# from fastapi_pagination.ext.sqlalchemy import paginate
# from fastapi_pagination import Params
# from pydantic import EmailStr
# from sqlalchemy.orm import Session, load_only
# from app.auth.jwt_handler import decode_jwt_token
# from app.hashing.password_hash import Hash
# from app.models.user_model import UserModel
# from config.database import get_db


# # New user register
# def create_user(name : str = Form(), email : EmailStr = Form(), password : str = Form(), city : str = Form(None), state : str = Form(None), country : str = Form(None), db: Session = Depends(get_db)):

#     try:
#         existing_user = db.query(UserModel).filter(UserModel.email == email).first()

#         if existing_user:
#             return None

#         new_user = UserModel(
#             name=name,
#             email=email,
#             password=Hash.bcrypt(password),
#             city=city,
#             state=state,
#             country=country,
#         )

#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except Exception as e:
#         print("Exception occured:", str(e))
#         return {"error": "Failed to create user"}




# # Get all user information
# def get_all_users(db: Session, params: Params, sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
#     try:
#         query = db.query(UserModel).options(load_only( UserModel.id, UserModel.email, UserModel.name, UserModel.city, UserModel.country, UserModel.state))

#         if sort_by:
#             sort_column = getattr(UserModel, sort_by, None)
#             if sort_column is None:
#                 raise ValueError(f"Invalid sort_by field: {sort_by}")

#             if sort_direction == "desc":
#                 query = query.order_by(sort_column.desc())
#             elif sort_direction == "asc":
#                 query = query.order_by(sort_column.asc())
#             else:
#                 query = query.order_by(UserModel.id.asc())
#         else:
#             query = query.order_by(UserModel.id.asc())

#         paginated_users = paginate(query, params=params)
#         return paginated_users

#     except Exception as e:
#         print("An exception occurred:", str(e))
#         return None




# # Get user information by id
# def show_user(id: int, db: Session):
#     try:
#         user = db.query(UserModel).options(load_only( UserModel.id, UserModel.name, UserModel.email, UserModel.city, UserModel.state, UserModel.country)).filter(UserModel.id == id).first()
        
#         if not user:
#             return None
#         return user
#     except Exception as e:
#         print("An exception occurred:", str(e))
#         return False




# # Update user
# def update_user_info(name: Optional[str],new_password: Optional[str],email: Optional[str],city: Optional[str],state: Optional[str],country: Optional[str],token: str,db: Session):
#     try:
#         user_email = decode_jwt_token(token)
#         user = db.query(UserModel).filter(UserModel.email == user_email).first()

#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#         if name is not None:
#             user.name = name

#         if new_password is not None:
#             if Hash.verify(user.password, new_password):
#                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different from the current password")
            
#             user.password = Hash.bcrypt(new_password)

#         if email is not None:
#             user.email = email

#         if city is not None:
#             user.city = city

#         if state is not None:
#             user.state = state

#         if country is not None:
#             user.country = country

#         db.commit()

#         return {
#             "name": user.name,
#             "email": user.email,
#             "city": user.city,
#             "state": user.state,
#             "country": user.country,
#         }

#     except Exception as e:
#         print("An exception occurred:", str(e))
#         return False




# # Delete user by id
# def delete_user_info(id: int, db: Session):
#     try:
#         user = db.query(UserModel).filter(UserModel.id == id).first()

#         if user is None:
#             return None

#         db.delete(user)
#         db.commit()
#         return user
#     except Exception as e:
#         print("Exception occurred:", str(e))
#         return False




from typing import List, Optional
from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy.orm import Session, load_only
from app.auth.jwt_handler import decode_jwt_token
from app.hashing.password_hash import Hash
from app.models.user_model import UserModel
from app.schemas.user_register_schema import UserRegisterSchema
from app.schemas.user_update_schema import UserUpdateSchema

# New user register
def create_user(user_data: UserRegisterSchema, db: Session):
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
        query = db.query(UserModel).options(load_only(UserModel.id, UserModel.email, UserModel.name, UserModel.city, UserModel.country, UserModel.state))

        if sort_by and sort_direction:
            if sort_direction == "desc":
                query = query.order_by(getattr(UserModel, sort_by).desc())
            elif sort_direction == "asc":
                query = query.order_by(getattr(UserModel, sort_by).asc())
        
        paginated_users = paginate(query, params=params)
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




# Update user
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
