import jwt  
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.models import User
from app.dependency import get_db
from app.utils.security import decode_access_token
from app.repository import users as users_repository

bearer_scheme = HTTPBearer()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        login = decode_access_token(creds.credentials)
    except (jwt.InvalidTokenError, KeyError):
        raise credentials_exc

    user = users_repository.get_user(db, "login", login)
    if user is None:
        raise credentials_exc
    return user
