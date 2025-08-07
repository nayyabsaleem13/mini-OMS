from passlib.context import CryptContext
import os
from datetime import datetime , timedelta
import jwt

SECRET_KEY = "56398$242£$%&234346546££^436rgfds43"
ALGORITHM = "HS256"
pwd_context= CryptContext(schemes=["bcrypt"],deprecated= "auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + timedelta(minutes=30)})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

