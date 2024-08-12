from sqlalchemy.orm import Session
from app.hashing.password_hash import Hash
from app.auth.jwt_handler import create_access_token, decode_jwt_token
from app.models.roles_model import Role
from app.models.user_model import UserModel

# user login
def login_user(email: str, password: str, db: Session):
    try:
        user = db.query(UserModel).filter(UserModel.email == email).first()

        if not user or not Hash.verify(user.password, password):
            return None
        
        # return the role of user
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role:
            return None
        
        access_token = create_access_token(data={"sub": user.email})

        return {
            "name": user.name,
            "email": user.email,
            "access_token": access_token,
            "role": role.role_name
        }
    
    except Exception as e:
        print("An exception occurred:", str(e))



# get user information by access token
def userinfo_by_token(token: str, db: Session):
    try:
        email = decode_jwt_token(token)
        
        if email is None:
            return None

        user = db.query(UserModel).filter(UserModel.email == email).first()
        
        if not user:
            return None

        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role:
            return None

        return {
            "name": user.name,
            "email": user.email,
            "password": user.password,  
            "role_id": user.role_id,
            "city": user.city,
            "state": user.state,
            "country": user.country,
            "role_name": role.role_name  
        }
    
    except Exception as e:
        print("An exception occurred:", str(e))