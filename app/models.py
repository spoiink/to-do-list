from sqlalchemy import ForeignKey, String, DateTime

from sqlalchemy.orm import Mapped, mapped_column

from app.dataBase import Base

from datetime import datetime




class User(Base):
    __tablename__= 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    login: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
    String(20),
    unique=True,
    nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )




class RefreshToken(Base):
    __tablename__= 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )