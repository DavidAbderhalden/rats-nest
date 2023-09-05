"""Top level application controller"""
from typing import Any

from fastapi import APIRouter

from .libs import accounts_controller, address_controller
from app.environments import settings as app_settings

api_controller = APIRouter(prefix='/api/v1')
api_controller.include_router(accounts_controller)
api_controller.include_router(address_controller)


@api_controller.get('/settings')
async def settings() -> dict[str, Any]:
    return {
        'status': 'ok',
        'username': app_settings.DATABASE_USER,
        'password': app_settings.DATABASE_PASSWORD,
        'host': app_settings.DATABASE_HOST,
        'port': app_settings.DATABASE_PORT,
        'name': app_settings.DATABASE_NAME
    }
