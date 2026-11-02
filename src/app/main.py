from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.api.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

