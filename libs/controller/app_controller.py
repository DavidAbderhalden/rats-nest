from fastapi import APIRouter, Depends
from libs.controller.items_controller import itemsController
from libs.environments.settings import Base
from libs import deps

appController = APIRouter(prefix='/api/v1')
appController.include_router(itemsController)

@appController.get('/hello/{username}')
async def hello(username: str):
    return {
        'status': 'ok',
        'message': f'Hello {username}!'
    }

@appController.get('/settings')
async def hello(settings: Base = Depends(deps.get_app_settings)):
    return {
        'status': 'ok',
        'url': settings.RANDOM_URL
    }
