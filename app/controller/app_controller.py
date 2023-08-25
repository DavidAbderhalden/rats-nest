"""Top level application controller"""
from typing import Any

from fastapi import APIRouter

from app.controller.libs import itemsController, accountsController
from app.environments import settings as app_settings

appController = APIRouter(prefix='/api/v1')
appController.include_router(itemsController)
appController.include_router(accountsController)

@appController.get('/hello/{username}')
async def hello(username: str):
    return {
        'status': 'ok',
        'message': f'Hello {username}!'
    }

@appController.get('/settings')
async def settings() -> dict[str, Any]:
    return {
        'status': 'ok',
        'username': app_settings.DATABASE_USER,
        'password': app_settings.DATABASE_PASSWORD,
        'host': app_settings.DATABASE_HOST,
        'port': app_settings.DATABASE_PORT,
        'name': app_settings.DATABASE_NAME
    }
