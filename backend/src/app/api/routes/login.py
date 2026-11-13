from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
from datetime import timedelta
from typing import Annotated 

from app.schemas.schema_token import TokenBase
from app.schemas.schema_user import UserPublic
from app.api.deps import SessionDep
from app.api.core import security
from app.api.core.config import settings
from app import curd

router = APIRouter(
    prefix="/login",
    tags=["login"],
)

@router.post("/access-token", response_model=TokenBase)
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenBase:
    user = curd.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)   
   
    return TokenBase(access_token=security.create_access_token(user.id, expires_delta=token_expires)
    )
    
