from sqlalchemy.orm import Session

from app.models import User
from typing import Literal


def get_user(db: Session, 
            kind: Literal["login", "id"], 
            value: str | int) -> User | None:
    if kind == 'login':
        return db.query(User).filter(User.login == value).scalar()
    if kind == 'id':
        return db.query(User).filter(User.id == value).scalar()


def create_user(
    db: Session,
    login: str,
    username: str,
    hashed_password: str,
) -> User:
    user = User(
        login=login,
        username=username,
        hashed_password=hashed_password,
    )
    db.add(user)  # добавляет объект в сессию, но не отправляет SQL-запрос немедленно
    db.flush()    # отправляет изменения в БД в рамках текущ транзакции. Ex: позволяет получить сген user.id
    return user   # перечитывает данные объекта из БД
