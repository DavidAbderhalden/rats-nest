from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from libs.services.database_operations import DatabaseOperationsService, get_database_operations_service

itemsController = APIRouter(prefix='/items')

@itemsController.get('/count')
async def count(
        database_operations_service: Annotated[DatabaseOperationsService, Depends(get_database_operations_service)],
):
    session = database_operations_service.get_session()

    return {
        'status': 'ok',
        'counter': f'{session} requests have been sent.'
    }
