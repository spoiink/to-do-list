from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repository.profile import get_current_user
from app.schemas import ProfileUpdate, UserResponse, UserProfile, PROFILE_UPDATE_EXAMPLES
from app.models import User
from app.dependency import get_db
from app.service import profile as profile_service


router = APIRouter()


@router.get("/profile/me", response_model=UserProfile)   # Читаем профиль
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user     

@router.patch("/profile/me", response_model=UserProfile)   # Меняем отдельные поля профиля
def update_profile(
    data: Annotated[ProfileUpdate, Body(openapi_examples=PROFILE_UPDATE_EXAMPLES)],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return profile_service.update_profile(db, current_user, data)


@router.put("/profile/avatar", response_model=UserResponse)  # Загружаем или заменяем аватар. Принимай UploadFile
def ava():
    pass

@router.delete("/profile/avatar", response_model=UserResponse)  # Удаляем аватар
def d_av():
    pass

@router.patch("/profile/password", response_model=UserResponse)   # Меняем пароль
def ch_pw(old_pwd, new_pwd):
    pass