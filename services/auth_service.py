# services/auth_service.py
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.database import db, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


def hash_password(password: str):
    # bcrypt only supports passwords up to 72 characters
    if not isinstance(password, str):
        password = str(password)
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    # bcrypt only supports passwords up to 72 characters
    if not isinstance(password, str):
        password = str(password)
    password = password[:72]
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----- DB operations -----
async def create_user(user_data: dict):
    user_data["password"] = hash_password(user_data["password"])
    user_data.setdefault("is_active", True)
    user_data.setdefault("role", "company_admin")  # default role
    result = await db["users"].insert_one(user_data)
    return str(result.inserted_id)


async def find_user_by_email(email: str):
    return await db["users"].find_one({"email": email})


# ----- Auth dependency -----
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await db["users"].find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 👇 Quick debug print
        print(f"🔑 Current user: {user.get('email')} | Role: {user.get('role')}")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

