from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repository.profile import get_current_user
from schemas import UserResponse, UserProfile
from app.models import User
from app.dependency import get_db



router = APIRouter()


@router.get("/profile/me", response_model=UserProfile)   # Читаем профиль
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user     

@router.patch("/profile", response_model=UserResponse)   # Меняем отдельные поля профиля 
def bio():
    pass

@router.put("/profile/avatar", response_model=UserResponse)  # Загружаем или заменяем аватар
def ava():
    pass

@router.delete("/profile/avatar", response_model=UserResponse)  # Удаляем аватар
def d_av():
    pass

@router.patch("/profile/password", response_model=UserResponse)   # Меняем пароль
def ch_pw():
    pass