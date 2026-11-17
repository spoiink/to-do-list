from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session



from app.schemas import TokenPair
from app.models import User
from app.repository import ref_token as ref_token_repos
from app.repository.users import get_user
from app.utils.security import create_refresh_token, hash_refresh_token, create_access_token, REFRESH_TOKEN_EXPIRE_DAYS

def issue_token_pair(db: Session, user: User) -> TokenPair:   #  # Генерируем refresh token
    raw = create_refresh_token()
    ref_token_repos.add_refresh_token(
        db, 
        user.id, 
        hash_refresh_token(raw), 
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),   # Рассчитываем срок действия
        )
    
    return TokenPair(
        access_token=create_access_token(user.login), 
        refresh_token=raw
        )



def refresh_token_pair(db: Session, raw_token: str) -> TokenPair:
    token_hash = hash_refresh_token(raw_token)
    token = ref_token_repos.get_by_hash(db, token_hash)

    if token is None:
        raise HTTPException(401, "Invalid refresh token")

    if token.revoked_at is not None:
        ref_token_repos.revoke_all_for_user(db, token.user_id)
        raise HTTPException(401, "Refresh token revoked")

    if token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(401, "Refresh token expired")  #^

    user = get_user(db, "id", token.user_id)    # Если пользователя удалили, а реф-токен остался
    if user is None:
        raise HTTPException(401, "User not found")

    if not ref_token_repos.revoke_by_hash(db, token_hash):
        raise HTTPException(401, "Refresh token already used")

    return issue_token_pair(db, user)
    
