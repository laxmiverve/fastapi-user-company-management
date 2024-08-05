from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.helper.email_config import email_settings
import smtplib
import random


class Helper:
    def generate_otp():
        otp = random.randint(100000, 999999)
        return otp


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
