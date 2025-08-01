from models.user_model import User
from utils.security import hash_password, verify_password, create_access_token
from schemas.user_schema import UserLogin
from fastapi import HTTPException

async def register_user(email: str, password: str, username: str):
    existing = await User.find_one(User.email == email)
    if existing:
        raise HTTPException(status_code=400, detail="email sudah terdaftar")
    
    user = User(email=email, password_hash=hash_password(password), username=username)
    await user.insert()
    return {"message": "pengguna berhasil terdaftar"}

async def login_user(user_data: UserLogin):
    user = await User.find_one(User.email == user_data.email)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="email atau password salah")
    
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
