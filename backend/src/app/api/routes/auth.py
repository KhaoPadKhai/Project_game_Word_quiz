from tkinter import Message
from typing import Any
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from app.schemas.schema_user import UserPublic, UserRegister

from app import curd
from app.api.deps import Current_userDep, SessionDep
from app.schemas.schema_token import Message

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/create-user", response_model=UserPublic)
def create_user(session: SessionDep, user_create: UserRegister):
    user = curd.get_user_by_email(session, email= user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    user = curd.create_user(session, user_create)
    return user
        
@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: Current_userDep) -> Any:
    return current_user

@router.post("/logout", response_model=Message)
def logout(current_user: Current_userDep) -> Message:
    return Message(message="Logged out successfully")