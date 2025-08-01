from fastapi import APIRouter, Depends
from schemas.user_schema import UserRegister, UserLogin, TokenResponse
from services.auth_service import register_user, login_user
from models.user_model import User
from utils.security import get_current_user

router = APIRouter()

@router.post("/register")
async def register(data: UserRegister):
    return await register_user(data.email, data.password, data.username)

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    return await login_user(data)

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}

