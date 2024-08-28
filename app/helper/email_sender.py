from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import Depends, HTTPException, Header, Request
from requests import Session
from app.auth.jwt_handler import decode_jwt_token
from app.helper.email_config import email_settings
import smtplib
import random
from config.database import get_db
from sqlalchemy.orm import Session
from app.models.company_model import CompanyModel
from config.database import get_db
from app.models.user_model import UserModel


class Helper:
    # generate 6 digit OTP
    def generate_otp():
        otp = random.randint(100000, 999999)
        return otp


    # sent the forget password OTP to mail
    def send_email(receiver_email, otp):
        try:
            sender_email = email_settings.email_user
            subject = "Your OTP"
            body = f"OTP for forget password is: {otp}"

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))
        
            with smtplib.SMTP(email_settings.email_host, email_settings.email_port) as server:
                server.starttls()
                server.login(sender_email, email_settings.email_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Email sent to {receiver_email}")
        except Exception as e:
            print(f"Failed to send email to {receiver_email}: {str(e)}")

        
    
    # sent the successful registration mail 
    def regd_mail_send(receiver_email: str):
        try:
            sender_email = email_settings.email_user

            subject = 'Registration Successful'
            body = "Your registration was successful"

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            
            with smtplib.SMTP(email_settings.email_host, email_settings.email_port) as server:
                server.starttls()
                server.login(sender_email, email_settings.email_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                # server.send_message(msg)
            print(f'Email sent to {receiver_email}')
            
        except Exception as e:
            print(f"Failed to send email to {receiver_email}: {str(e)}")

    

    # def getAuthUser(request: Request, db: Session = Depends(get_db)):
    #     try:
    #         authorization: str = request.headers.get("Authorization")
            
    #         if not authorization or not authorization.startswith("Bearer "):
    #             raise HTTPException(status_code=401, detail="Authorization header missing or malformed")

    #         token = authorization.split(" ")[1]
            
    #         email = decode_jwt_token(token)
    #         if not email:
    #             raise HTTPException(status_code=401, detail="Invalid or expired token")

    #         user = db.query(UserModel).filter(UserModel.email == email).first()

    #         if not user:
    #             raise HTTPException(status_code=404, detail="User not found")

    #         return user
    #     except Exception as e:
    #         print("Exception occurred:", str(e))
    #         raise HTTPException(status_code=500, detail="An internal error occurred")
        
        

    # def company_header_dependency(request: Request, Uuid: str = Header(None), db: Session = Depends(get_db)):
    #     try:
    #         user = Helper.getAuthUser(request=request, db=db)
            
    #         user_roles = [role.id for role in user.roles] if user.roles else []
            
    #         if 1 not in user_roles: 
    #             company = db.query(CompanyModel).filter(CompanyModel.uuid == Uuid).first()
                
    #             if company:
    #                 return company.id  
    #             else:
    #                 raise HTTPException(status_code=404, detail="Company not found")
    #         else:
    #             raise HTTPException(status_code=403, detail="Not authorized to access this company")
    #     except Exception as e:
    #         print("Exception occurred:", str(e))

