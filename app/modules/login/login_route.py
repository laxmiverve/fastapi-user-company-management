from typing import Optional
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.modules.login import user_login_service
from app.schemas.user_response_schema import UserInformationSchema
from config.database import get_db, msg
from app.schemas.response_schema import ResponseSchema
from app.schemas.user_login_schema import LoginSchema, LoginResponseSchema


router = APIRouter(prefix="/user", tags=["Login"])

# User login
@router.post('/login', summary="User login", response_model = ResponseSchema[LoginResponseSchema])
def login_user(login_data: LoginSchema, db: Session = Depends(get_db)):
    logged_user = user_login_service.login_user(email = login_data.email, password = login_data.password, db = db)
    if logged_user == 1:
        return ResponseSchema(status = False, response = msg['invalid_email_format'], data = None)
    if logged_user is not None:
        return ResponseSchema(status = True, response = msg['user_login'], data = logged_user)
    else:
        return ResponseSchema(status = False, response = msg['user_not_authorized'], data = None)



# Get user information by access token
@router.get("/info", summary="Get User Information", response_model=ResponseSchema[UserInformationSchema])
def get_user_info(token: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user_info = user_login_service.userinfo_by_token(token=token, db=db)
    
    if user_info == 1:
        return ResponseSchema(status=False, response=msg['access_token_not_found'], data=None)
    elif user_info:
        return ResponseSchema(status=True, response=msg['user_info_found'], data=user_info)
    else:
        return ResponseSchema(status=False, response=msg["invalid_token"], data=None)
