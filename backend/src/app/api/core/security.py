from datetime import datetime, UTC, timedelta
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing import Any
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from app.api.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

password_hash = PasswordHash((Argon2Hasher(),))

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


ALGORITHM = "HS256"

def create_access_token(subject: str| Any, expires_delta: timedelta | None = None) -> str:
    expires = datetime.now(UTC) + expires_delta
    to_encode = {"exp": expires, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    