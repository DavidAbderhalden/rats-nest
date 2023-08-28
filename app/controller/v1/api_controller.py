"""Top level application controller"""
from typing import Any

from fastapi import APIRouter

from .libs import accounts_controller
from app.environments import settings as app_settings

api_v1_controller = APIRouter(prefix='/api/v1')
api_v1_controller.include_router(accounts_controller)

@api_v1_controller.get('/hello/{username}')
async def hello(username: str):
    return username

@api_v1_controller.get('/settings')
async def settings() -> dict[str, Any]:
    return {
        'status': 'ok',
        'username': app_settings.DATABASE_USER,
        'password': app_settings.DATABASE_PASSWORD,
        'host': app_settings.DATABASE_HOST,
        'port': app_settings.DATABASE_PORT,
        'name': app_settings.DATABASE_NAME
    }
