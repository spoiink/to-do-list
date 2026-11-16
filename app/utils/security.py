import os
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
import hashlib, secrets


REFRESH_TOKEN_EXPIRE_DAYS = 7


SECRET_KEY = os.environ["SECRET_KEY"]   # длинная случайная строка, не в коде и не в git
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(login: str) -> str:
    payload = {
        "sub": login,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    # проверяет подпись и exp; при проблеме бросает исключение
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]




def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)   # случайная строка, не JWT. secrets generate random symbols


def hash_refresh_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()     # 'raw.encode()'m превращает строку в байты
