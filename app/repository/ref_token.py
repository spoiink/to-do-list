# repository/ref_token.py
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import RefreshToken


def add_refresh_token(db: Session, user_id: int, token_hash: str, expires_at: datetime) -> None:
    db.add(RefreshToken(
        user_id=user_id, 
        token_hash=token_hash, 
        expires_at=expires_at)
    )
    db.commit()


def get_by_hash(db: Session, token_hash: str) -> RefreshToken | None:
    return db.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))


def revoke_by_hash(db: Session, token_hash: str) -> None:
    result = db.execute(
        update(RefreshToken)
        .where(RefreshToken.token_hash == token_hash, 
               RefreshToken.revoked_at.is_(None))
        .values(revoked_at=datetime.now(timezone.utc))
    )
    db.commit()
    return result.rowcount > 0

def revoke_all_for_user(db: Session, user_id: int) -> None:
    db.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
        .values(revoked_at=datetime.now(timezone.utc))
    )
    db.commit()