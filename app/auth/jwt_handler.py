from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
hashing_algorithm = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 120

# create the access token 
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm = hashing_algorithm)
    return encoded_jwt


# decode the access token 
def decode_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms = [hashing_algorithm])
        email: str = decoded_token.get("sub")
        return email
    except JWTError:
        return None
