import warnings
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Self
from pydantic import EmailStr, HttpUrl, field_validator, model_validator, computed_field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    PROJECT_NAME: str
    SECRET_KEY: str
    
# ขั้นที่ 2 
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    FASTAPI_ENV: Literal["development"] | None = None

    SENTRY_DSN: HttpUrl | None # คืออะไรติดไว้ก่อน
    # ขั้นที่ 3 ตรวจสอบว่า url เป็นแบบไหน ใช่ "postgres://", "postgresql://" ถ้าใช่ จะเปลี่ยนเป็น postgresql+psycopg:// แทน
    DATABASE_URL: str = "sqlite:///./app.db" # PostgresDsn
    
    
    # ขั้นที่ 5 set default email
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None
    
    @field_validator("DATABASE_URL", mode= "before") 
    @classmethod
    def _use_psycopg_driver(cls, value: str ) -> str: # มาเปลี่ยนเป็น PostgresDsn และที่ใช้ cls เพราะเป็นการทำก่อนจะมี ค่า คือการเตรียมค่า
        database_url = str(value)
        for scheme in ("postgres://", "postgresql://"):
            if database_url.startswith(scheme):
                return database_url.replace(scheme, "postgresql+psycopg://", 1)
        return database_url
    @model_validator(mode="after") #@model_validator คือ ใช้หลายฟิวล์ มาเปลี่ยนค่าหรือทำอะไรสักอย่าง
    def set_default_email(self) -> Self:
        if not Self.EMAILS_FROM_NAME:
            Self.EMAILS_FROM_NAME = Self.PROJECT_NAME
        return Self
        
    # ขั้นที่ 6     
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587 
    SMTP_HOST: str | None = None # SMTP server // email
    SMTP_USER: str | None = None # SMTP server // email
    SMTP_PASSWORD: str | None = None 

    
    @computed_field
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)
    
    def _check_default_secret(self, var_name:str, value:str | None ) -> None:
        if value == "deaw":
            message = (
                f'The value of {var_name} is "deaw", '
                "for security, please change it, at least for deployments.")
            if self.FASTAPI_ENV == "development":
                    warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)
    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        return self
    
    
settings = Settings()
    