from pydantic import BaseModel, EmailStr

class SentOtpResponseSchema(BaseModel):
    otp: int
    message: str


class VerifyOtpResponseSchema(BaseModel):
    message: str


class ChangePasswordResponseSchema(BaseModel):
    message: str

    class Config:
        from_attributes = True