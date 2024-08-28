from pydantic import BaseModel, EmailStr

class SentForgotPasswordOTPSchema(BaseModel):
    # email:EmailStr
    email: str

class VerifyForgotPasswordOTPSchema(BaseModel):
    # email: EmailStr
    email: str
    otp: int

class ChangePasswordSchema(BaseModel):
    # email:EmailStr
    email: str
    otp: int
    new_password:str
    confirm_password:str


# response schemas
class SentOtpResponseSchema(BaseModel):
    otp: int
    message: str

class VerifyOtpResponseSchema(BaseModel):
    message: str

class ChangePasswordResponseSchema(BaseModel):
    message: str

    class Config:
        from_attributes = True