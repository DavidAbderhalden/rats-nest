from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from libs.controller.items_controller import itemsController
from libs.environments.settings import Base, get_app_settings

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
    settings: Annotated[Base, Depends(get_app_settings)]
):
    return {
        'status': 'ok',
        'username': settings.DATABASE_USER,
        'password': settings.DATABASE_PASSWORD,
        'host': settings.DATABASE_HOST,
        'port': settings.DATABASE_PORT,
        'name': settings.DATABASE_NAME
    }
