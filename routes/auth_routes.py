from fastapi import APIRouter, HTTPException
from models.user import UserSignup, UserLogin
from services import auth_service

router = APIRouter()

# Signup route
@router.post("/signup")
async def signup(user: UserSignup):
    existing_user = await auth_service.find_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_id = await auth_service.create_user(user_dict)
    return {"message": "User created successfully", "user_id": user_id}


# Login route
@router.post("/login")
async def login(user: UserLogin):
    db_user = await auth_service.find_user_by_email(user.email)
    # Debug prints to help diagnose login issues
    print("DB user:", db_user)
    print("Input password:", user.password)
    print("Stored password:", db_user["password"] if db_user else None)
    if not db_user or not auth_service.verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_service.create_access_token({"sub": db_user["email"], "role": db_user["role"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user["role"],   # 👈 send role for frontend redirection
    }
