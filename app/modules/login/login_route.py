# from fastapi import APIRouter, Depends, Form
# from app.schemas.response_schema import ResponseSchema
# from config.database import get_db, msg
# from sqlalchemy.orm import Session
# from app.modules.login import user_login_service


# router = APIRouter(tags=["Login"])


# @router.post('/user/login', summary="User login")
# def login_user(email: str = Form(), password: str = Form(), db: Session = Depends(get_db)
# ):
#     logged_user = user_login_service.login_user(email = email, password = password, db = db)
   
#     if logged_user is not None:
#         return ResponseSchema(status = True, response = msg['user_login'], data = logged_user)
#     else:
#         return ResponseSchema(status = False, response = msg['user_not_authorized'], data = None)
    




from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.login import user_login_service
from config.database import get_db, msg
from app.schemas.response_schema import ResponseSchema
from app.schemas.user_login_schema import LoginSchema, LoginResponseSchema


router = APIRouter(tags=["Login"])

# # User login
# @router.post('/user/login', summary="User login", response_model = ResponseSchema[UserSchema])
# def login_user(login_data: LoginSchema, db: Session = Depends(get_db)):
#     logged_user = user_login_service.login_user(email = login_data.email, password = login_data.password, db = db)

#     if logged_user is not None:
#         return ResponseSchema(status = True, response = msg['user_login'], data = logged_user)
#     else:
#         return ResponseSchema(status = False, response = msg['user_not_authorized'], data = None)
    
@router.post('/user/login', summary="User login", response_model = ResponseSchema[LoginResponseSchema])
def login_user(login_data: LoginSchema, db: Session = Depends(get_db)):
    logged_user = user_login_service.login_user(email = login_data.email, password = login_data.password, db = db)

    if logged_user is not None:
        return ResponseSchema(status = True, response = msg['user_login'], data = logged_user)
    else:
        return ResponseSchema(status = False, response = msg['user_not_authorized'], data = None)