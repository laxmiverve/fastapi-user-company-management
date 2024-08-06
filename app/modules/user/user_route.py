# from typing import Optional
# from fastapi import APIRouter, Depends, Form
# from pydantic import EmailStr
# from app.modules.user import user_service
# from config.database import get_db, msg
# from sqlalchemy.orm import Session
# from app.schemas.response_schema import ResponseSchema
# from app.auth.jwt_bearer import JWTBearer   
# from fastapi_pagination import Params


# router = APIRouter(tags=["User"])

 
# # New user register
# @router.post('/user/register', summary = "Register new users")
# def register_user(name : str = Form(), email : EmailStr = Form(), password : str = Form(), city : str = Form(None), state : str = Form(None), country : str = Form(None), db: Session = Depends(get_db)):
    
#     new_user = user_service.create_user(name = name, email = email, password = password, city = city, state = state, country = country, db = db) 
#     if new_user is not None:
#         return ResponseSchema(status = True, response = msg['user_register'], data = new_user.__dict__)
#     else:
#         return ResponseSchema(status = False, response = msg['user_already_exists'], data = None)
 


# # Get all user information 
# @router.get("/user/list", summary="List of users", dependencies = [Depends(JWTBearer())])
# def read_users(params: Params = Depends(), db: Session = Depends(get_db), sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
#     all_users = user_service.get_all_users(db = db, params=params, sort_by = sort_by, sort_direction = sort_direction)

#     if all_users is not None:
#         return ResponseSchema(status = True, response = msg['user_list_found'], data = all_users)
#     else:
#         return ResponseSchema(status = False, response = msg['user_list_not_found'], data = None)



# # Get user information by id 
# @router.get('/user/{id}', summary = "Get user", dependencies = [Depends(JWTBearer())])
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = user_service.show_user(id = id, db = db)
    # if user is not None:
    #     return ResponseSchema(status = True, response = msg['get_user_by_id'], data = user.__dict__)
    # else:
    #     return ResponseSchema(status = False, response = msg['get_user_by_id_not_found'], data = None)



# # Delete user by id
# @router.delete('/user/delete/{id}', summary = "Delete user", dependencies = [Depends(JWTBearer())])
# def delete_user(id: int, db: Session = Depends(get_db)):
#     delete_user = user_service.delete_user_info(id = id, db = db)
    # if delete_user is not None: 
    #     return ResponseSchema(status = True, response = msg['delete_user_by_id'], data = delete_user.__dict__)
    # else:
    #     return ResponseSchema(status = False, response = msg['delete_user_by_id_not_found'], data = None)



# # Update user
# @router.put('/user/update', summary = "Update user", dependencies = [Depends(JWTBearer())])
# def update_user_info(name: Optional[str] = Form(None), new_password: Optional[str] = Form(None), email: Optional[str] = Form(None), city: Optional[str] = Form(None), state: Optional[str] = Form(None), country: Optional[str] = Form(None), token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):

#     update_user = user_service.update_user_info(name = name, new_password = new_password, email = email, city = city, state = state, country = country, token = token, db = db)
    
    # if update_user:
    #     return ResponseSchema(status = True, response = msg['update_current_logged_user'], data = update_user)
    # else:
    #     return ResponseSchema(status = False, response = msg['update_current_logged_user_error'], data = None)




from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi_pagination import Params
from app.modules.user import user_service
from config.database import get_db, msg
from app.schemas.response_schema import ResponseSchema
from app.auth.jwt_bearer import JWTBearer
from app.schemas.user_register_schema import UserRegisterSchema
from app.schemas.user_update_schema import UserUpdateSchema
from app.schemas.user_response_schema import UserResponseSchema

router = APIRouter(tags=["User"])


# New user register
@router.post('/user/register', summary="Register new users", response_model = ResponseSchema[UserResponseSchema])
def register_user(user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    new_user = user_service.create_user(user_data = user_data, db = db)
    if new_user is not None:
        return ResponseSchema(status = True, response = msg['user_register'], data = new_user.__dict__)
    else:
        return ResponseSchema(status = False, response = msg['user_already_exists'], data = None)
        



# Get all user information
# @router.get("/user/list", summary="List of users", dependencies=[Depends(JWTBearer())])
@router.get("/user/list", summary="List of users", response_model = ResponseSchema[List[UserResponseSchema]], dependencies = [Depends(JWTBearer())])
def read_users(params: Params = Depends(), db: Session = Depends(get_db), sort_by: Optional[str] = None, sort_direction: Optional[str] = None):
    all_users = user_service.get_all_users(db=db, params=params, sort_by=sort_by, sort_direction=sort_direction)
    if all_users:
        return ResponseSchema(status=True, response=msg['user_list_found'], data=all_users.items) 
    else:
        return ResponseSchema(status=False, response=msg['user_list_not_found'], data=None)






# Get user information by id
# @router.get('/user/{id}', summary="Get user", dependencies=[Depends(JWTBearer())])
@router.get('/user/{id}', summary="Get user",  response_model = ResponseSchema[UserResponseSchema], dependencies = [Depends(JWTBearer())])

def get_user(id: int, db: Session = Depends(get_db)):
    user = user_service.show_user(id = id, db = db)
    if user is not None:
        return ResponseSchema(status = True, response = msg['get_user_by_id'], data = user.__dict__)
    else:
        return ResponseSchema(status = False, response = msg['get_user_by_id_not_found'], data = None)





# Delete user by id
# @router.delete('/user/delete/{id}', summary="Delete user", dependencies=[Depends(JWTBearer())])
@router.delete('/user/delete/{id}', summary="Delete user", response_model = ResponseSchema[UserResponseSchema], dependencies = [Depends(JWTBearer())])

def delete_user(id: int, db: Session = Depends(get_db)):
    delete_user = user_service.delete_user_info(id = id, db = db)
    if delete_user is not None: 
        return ResponseSchema(status = True, response = msg['delete_user_by_id'], data = delete_user.__dict__)
    else:
        return ResponseSchema(status = False, response = msg['delete_user_by_id_not_found'], data = None)





# Update user
# @router.put('/user/update', summary="Update user", dependencies=[Depends(JWTBearer())])
@router.put('/user/update', summary="Update user",  response_model = ResponseSchema[UserResponseSchema], dependencies = [Depends(JWTBearer())])

def update_user_info(user_update_data: UserUpdateSchema, token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    update_user = user_service.update_user_info(user_update_data = user_update_data, token = token, db = db)
    if update_user:
        return ResponseSchema(status = True, response = msg['update_current_logged_user'], data = update_user.__dict__)
    else:
        return ResponseSchema(status = False, response = msg['update_current_logged_user_error'], data = None)

