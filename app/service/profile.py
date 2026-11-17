from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import ProfileUpdate
from app.repository import users as users_repository





def update_profile(db: Session, user: User, data: ProfileUpdate) -> User:
    fields = data.model_dump(exclude_unset=True)

    new_username = fields.get("username")
    if new_username is not None:
        if new_username == user.username:
            raise HTTPException(400, "Новый username совпадает с текущим")
        if users_repository.get_user(db, "username", new_username):
            raise HTTPException(409, "Этот username уже занят")

    return users_repository.update_user(db, user, fields)
