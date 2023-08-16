from fastapi import APIRouter, Depends
from libs.services.database_operations import DatabaseOperationsService
from libs.deps import get_database_operations_service

itemsController = APIRouter(prefix='/items')

@itemsController.get('/count')
async def count(database_operations_service: DatabaseOperationsService = Depends(get_database_operations_service)):
    database_operations_service.add(1)
    counter: int = database_operations_service.get_counter()
    return {
        'status': 'ok',
        'counter': f'{counter} requests have been sent.'
    }
