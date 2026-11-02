from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    email: EmailStr = Field(index=True, nullable=False, unique=True)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    full_name: str | None = Field(default=None, max_length=255)


class UserCreateAdmin(UserBase):
    password: str = Field(nullable=False)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)