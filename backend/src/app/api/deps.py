from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from typing import Annotated
from collections.abc import Generator
from sqlmodel import Session
from pydantic import ValidationError
from jwt.exceptions import PyJWTError
import jwt
import uuid

from app.api.core import security
from app.api.core.connect_db import engine
from app.api.core.config import settings
from app.models.model_user import User
from app.schemas.schema_token import Token_payload


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_db() -> Generator[Session]: 
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = Token_payload(**payload)
        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials"
            )
        user_id = uuid.UUID(token_data.sub)
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user
Current_userDep = Annotated[User, Depends(current_user)]