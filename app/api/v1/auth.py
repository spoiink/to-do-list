from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.service.auth import create_user
from app.schemas import (UserRegister, UserResponse, 
                         LoginRequest, RefreshSchema, TokenPair)
from app.dependency import get_db
from app.models import RefreshToken, User
from app.repository import users as users_repository
from app.repository import ref_token as ref_token_repos
from app.utils.security import (create_refresh_token, verify_password, create_access_token, 
                                hash_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS)
from app.service.ref_token import issue_token_pair, refresh_token_pair


router = APIRouter()


@router.post("/auth", response_model=UserResponse)
def auth_user(payload: UserRegister, db: Session = Depends(get_db)):
    return create_user(db, payload)

@router.post("/auth/login", response_model=TokenPair)        # выдаем пару токенов при регистрации или входе
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = users_repository.get_user(db, "login", data.login)

    if not user or not verify_password(data.password, user.hashed_password):
        # одно и то же сообщение, чтобы не подсказывать, что именно неверно
        raise HTTPException(status_code=401, detail="Incorrect login or password")
   
    return issue_token_pair(db, user)



@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshSchema, db: Session = Depends(get_db)):
    return refresh_token_pair(db, body.refresh_token)



@router.post("/logout", status_code=204)
def logout(body: RefreshSchema, db: Session = Depends(get_db)):
    ref_token_repos.revoke_by_hash(db, hash_refresh_token(body.refresh_token))