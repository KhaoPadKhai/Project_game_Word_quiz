from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.api.core.config import settings
from app.api.main import router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router, prefix=settings.API_V1_STR)