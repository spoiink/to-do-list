from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository import users as users_repository
from app.schemas import UserRegister, UserResponse
from app.utils.security import hash_password


def create_user(
        db: Session, 
        user_data: UserRegister,
) -> UserResponse:
    if users_repository.get_user(db, "login", user_data.login):
        raise HTTPException(
            status_code=400, 
            detail='User already exists'
        )

    hashed_password = hash_password(user_data.password)

    user = users_repository.create_user(
        db=db,
        login=user_data.login,
        username=user_data.username,
        hashed_password=hashed_password,
    )

    db.commit()
    db.refresh(user)
    
    return UserResponse.model_validate(user)