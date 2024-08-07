from typing import Dict, Tuple, Optional
from sqlalchemy.orm import Session
from app.helper.email_sender import Helper
from app.models.user_model import UserModel
from app.hashing.password_hash import Hash
from datetime import datetime, timedelta

otp_storage: Dict[str, Tuple[str, datetime]] = {}



# send forgot password OTP
def send_forgot_password_otp(email: str, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            return None
        
        otp = Helper.generate_otp()

        # store OTP and expiration time in the dictionary 
        expiration_time = datetime.now() + timedelta(minutes=15)
        otp_storage[email] = (otp, expiration_time)

        Helper.send_email(email, otp)
        return {
            "message": "OTP sent to the email",
            "otp": otp 
        }
    
    except Exception as e:
        print("Exception Occurred:", str(e))
        return None




# verify the OTP
def verify_otp(email: str, otp: int, db: Session):
    try:
        stored_data = otp_storage.get(email)

        if stored_data is None:
            return None  

        stored_otp, expiration_time = stored_data

        if datetime.now() > expiration_time:
            return {"message":"OTP was expired"} 
        
        if str(otp) == str(stored_otp):
            return {"message": "OTP is valid"}
       
    except Exception as e:
        print("Exception Occurred:", str(e))





# change user password
def change_password(email: str, otp: int, new_password: str, confirm_password: str, db: Session):
    try:
        stored_data = otp_storage.get(email)
        if not stored_data:
            return {"message": "Invalid OTP"}

        stored_otp, expiration_time = stored_data
        if datetime.now() > expiration_time:
            return {"message": "OTP has expired"}

        if str(otp) != str(stored_otp):
            return {"message": "OTP does not match"}

        get_db_user = db.query(UserModel).filter(UserModel.email == email).first()
        
        if not get_db_user:
            return {"message": "User not found"}

        if new_password != confirm_password:
            return {"message": "new password and confirm password do not match"}

        get_db_user.password = Hash.bcrypt(new_password)
        db.commit()

        del otp_storage[email] 

        return {"message": "Password changed successfully"}
        
    except Exception as e:
        print("Exception Occurred:", str(e))
        return None
