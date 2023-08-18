from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from app.libs.services.database_operations import DatabaseOperationsService, get_database_operations_service

itemsController = APIRouter(prefix='/items')

@itemsController.get('/count')
async def count(
        database_operations_service: Annotated[DatabaseOperationsService, Depends(get_database_operations_service)],
):

    return {
        'status': 'ok',
        'counter': 'requests have been sent.'
    }
