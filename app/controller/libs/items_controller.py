from fastapi import APIRouter

itemsController = APIRouter(prefix='/items')

@itemsController.get('/count')
async def count():
    return {
        'status': 'ok',
        'counter': 'requests have been sent.'
    }
