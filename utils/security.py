from typing import List
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from datetime import datetime , timedelta
import jwt
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from jwt import PyJWTError

from models import User

SECRET_KEY = "56398$242£$%&234346546££^436rgfds43"
ALGORITHM = "HS256"
auth_scheme = HTTPBearer()
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

async def get_current_user( credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= ALGORITHM)
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await User.find_one({"email":email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail= "Token could not be verified",headers={"WWW.Authenticate":"Bearer"})

