import uuid
from sqlmodel import SQLModel, Field
from datetime import UTC, datetime
from sqlalchemy import DateTime
from app.schema.schema_user import UserBase

def get_datetime_utc() -> datetime:
    return datetime.now(UTC)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True), 
    )