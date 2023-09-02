"""The base controller provides essential controller functionality and is consumed by controllers."""
from typing import TypeVar, Generic

from starlette import status

from fastapi.exceptions import HTTPException

from app.services import databaseOperationsService, DatabaseOperationsResult

_SchemaTypeT = TypeVar('_SchemaTypeT')
_ModelTypeT = TypeVar('_ModelTypeT')


class BaseController:
    _provider_name: str

    def __init__(self, provider_name: str):
        self._provider_name = provider_name

    async def create(
            self,
            body: _SchemaTypeT,
            model_type: Generic[_ModelTypeT],
            get_if_existing: bool = False
    ) -> Generic[_ModelTypeT]:
        if get_if_existing:
            database_operations_result: DatabaseOperationsResult[model_type] = \
                await databaseOperationsService.get_or_create(body, model_type=model_type)
        else:
            database_operations_result: DatabaseOperationsResult[model_type] = \
                await databaseOperationsService.create(body, model_type=model_type)
        if database_operations_result.name == 'database-error':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Creation terminated due to an invalid entity, {self._provider_name}"
            )
        return database_operations_result.data
