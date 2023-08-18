from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from app.libs.controller.items_controller import itemsController
from app.libs.environments.settings import Settings, get_app_settings

appController = APIRouter(prefix='/api/v1')
appController.include_router(itemsController)

@appController.get('/hello/{username}')
async def hello(username: str):
    return {
        'status': 'ok',
        'message': f'Hello {username}!'
    }

@appController.get('/settings')
async def hello(
    settings: Annotated[Settings, Depends(get_app_settings)]
):
    return {
        'status': 'ok',
        'username': settings.DATABASE_USER,
        'password': settings.DATABASE_PASSWORD,
        'host': settings.DATABASE_HOST,
        'port': settings.DATABASE_PORT,
        'name': settings.DATABASE_NAME
    }
