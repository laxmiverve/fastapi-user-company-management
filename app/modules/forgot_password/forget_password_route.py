# from fastapi import APIRouter, Depends, Form
# from sqlalchemy.orm import Session
# from app.modules.forgot_password import forget_password_service
# from app.schemas.response_schema import ResponseSchema
# from config.database import get_db, msg


# router = APIRouter(tags=["Forgot Password"])


# @router.post("/otp_sent", summary = "Send forgot password OTP")
# def forgot_password(email: str = Form(), db: Session = Depends(get_db)):
#     forget_pwd = forget_password_service.send_forgot_password_otp(email = email, db = db)
#     if forget_pwd is not None:
#         return ResponseSchema(status = True, response = msg['sent_otp'], data = forget_pwd)
#     else:
#         return ResponseSchema(status = False, response = msg['sent_otp_error'], data = None)



# @router.post("/otp_verify", summary = "Verify the OTP")
# def otp_verification( email: str = Form(), otp: int = Form(), db: Session = Depends(get_db)):
#     otp_verify = forget_password_service.verify_otp(email = email, otp = otp, db = db)
#     if otp_verify is not None:
#     # if type(otp_verify) != int:
#         return ResponseSchema(status = True, response = msg['otp_verified'], data = otp_verify)
#     else:
#         return ResponseSchema(status = False, response = msg['otp_verify_error'], data = {"message": "OTP is invalid"})
    
    

# @router.post("/change_password", summary = "Change user password")
# def change_user_password(email: str = Form(), otp: int = Form(), new_password: str = Form(), confirm_password: str = Form(), db: Session = Depends(get_db)):
#     password_change = forget_password_service.change_password( email = email, otp = otp, new_password = new_password, confirm_password = confirm_password, db = db)

#     if password_change is not None:
#         message = password_change.get("message")
        
#         if message == msg['change_password_success']:
#             return ResponseSchema(status = True, response = message, data = password_change)
#         else:
#             return ResponseSchema(status = False, response = message, data = None)
#     else:
#         return ResponseSchema(status = False, response = msg['change_password_error'], data = None)






from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.forgot_password import forget_password_service
from app.schemas.response_schema import ResponseSchema
from app.schemas.user_forget_password_schema import *
from app.schemas.forget_password_response_schema import *
from config.database import get_db, msg

router = APIRouter(tags=["Forgot Password"])

# send forgot password OTP
@router.post("/otp_sent", summary = "Send forgot password OTP", response_model = ResponseSchema[SentOtpResponseSchema])
def forgot_password(request: SentForgotPasswordOTPSchema, db: Session = Depends(get_db)):
    forget_pwd = forget_password_service.send_forgot_password_otp(email = request.email, db = db)
    if forget_pwd is not None:
        return ResponseSchema(status = True, response = msg['sent_otp'], data = forget_pwd)
    else:
        return ResponseSchema(status = False, response = msg['sent_otp_error'], data = None)



# verify the OTP
@router.post("/otp_verify", summary = "Verify the OTP", response_model = ResponseSchema[VerifyOtpResponseSchema])
def otp_verification(request: VerifyForgotPasswordOTPSchema, db: Session = Depends(get_db)):
    otp_verify = forget_password_service.verify_otp(email = request.email, otp = request.otp, db = db)

    if otp_verify is not None:
        response_data = VerifyOtpResponseSchema(message="OTP is valid")
        return ResponseSchema(status = True, response = msg['otp_verified'], data = response_data)
    else:
        response_data = VerifyOtpResponseSchema(message="Invalid OTP")
        return ResponseSchema(status = False, response = msg['otp_verify_error'], data = response_data)



# change user password
@router.post("/change_password", summary="Change user password", response_model = ResponseSchema[ChangePasswordResponseSchema])
def change_user_password(request: ChangePasswordSchema, db: Session = Depends(get_db)):
    password_change = forget_password_service.change_password(
        email = request.email,
        otp = request.otp,
        new_password = request.new_password,
        confirm_password = request.confirm_password,
        db = db
    )

    if password_change is not None:
        message = password_change.get("message")
        response_data = ChangePasswordResponseSchema(email = request.email, message = message)
        if message == msg['change_password_success']:
            return ResponseSchema(status = True, response = message, data = response_data)
        else:
            return ResponseSchema(status = False, response = message, data = response_data)
    else:
        response_data = ChangePasswordResponseSchema(email = request.email, message = "Password change failed.")
        return ResponseSchema(status = False, response = msg['change_password_error'], data = response_data)
    
