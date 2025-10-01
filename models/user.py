# models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: str   # "company_admin" | "dept_admin"
    name: str
    phone: Optional[str] = None
    department_id: Optional[str] = None
    is_active: bool = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
