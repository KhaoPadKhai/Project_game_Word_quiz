from sqlmodel import Session, select
from app.models.model_user import User
from app.schemas.schema_user import UserCreateAdmin
from app.api.core.security import get_password_hash, verify_password

def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def create_user(session: Session, user_create: UserCreateAdmin) -> User:
    user_db = User.model_computed_fields(user_create, update ={
        "email": user_create.email.lower(),
        "hashed_password": get_password_hash(user_create.password),
    })
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

DUMMY_HASH = get_password_hash("dummy_password")

def authenticate(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    if not user:
        verify_password(password, DUMMY_HASH) # กันการโจมตีแบบ timing attack โดยการตรวจสอบรหัสผ่านแม้ว่าผู้ใช้จะไม่มีอยู่จริง
        return None
    if not user.hashed_password:
        return None
    if not get_password_hash.verify(password, user.hashed_password):
        return None
    return user