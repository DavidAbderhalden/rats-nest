"""The base controller provides essential controller functionality and is consumed by controllers."""
from typing import TypeVar

from starlette import status

from fastapi.exceptions import HTTPException

from app.services import ServiceInterface, ServiceOperationsResult, ServiceOperationsSuccess

_RequestTypeT = TypeVar('_RequestTypeT')
_ResponseTypeT = TypeVar('_ResponseTypeT')


class BaseController:
    _provider_name: str
    _service: ServiceInterface

    def __init__(self, service_operations: ServiceInterface, provider_name: str):
        self._service_operations = service_operations
        self._provider_name = provider_name

    async def create(
            self,
            body: _RequestTypeT,
            response_model: _ResponseTypeT
    ) -> ServiceOperationsSuccess[_ResponseTypeT]:
        service_operations_result: ServiceOperationsResult[response_model] = await self._service_operations.create(
            request=body, response_model=response_model
        )
        if service_operations_result.name == 'service-error':
            # FIXME: Security issue, returns server error message. Somehow map the exceptions
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=service_operations_result.error
            )
        return service_operations_result
