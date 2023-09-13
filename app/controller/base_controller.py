"""The base controller provides essential controller functionality and is consumed by controllers."""
from typing import TypeVar

from fastapi.exceptions import HTTPException

from app.services import ServiceInterface, ServiceOperationsResult, ServiceOperationsSuccess
from app.utils import ExceptionMappingUtil

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
            response_model: _ResponseTypeT,
            **kwargs
    ) -> ServiceOperationsSuccess[_ResponseTypeT]:
        service_operations_result: ServiceOperationsResult[response_model] = await self._service_operations.create(
            request=body, response_model=response_model, background_task=kwargs.get('background_task')
        )
        return self._raise_errors(service_operations_result)

    async def read(
            self,
            body: _RequestTypeT,
            response_model: _ResponseTypeT,
    ) -> ServiceOperationsSuccess[_ResponseTypeT]:
        service_operations_result: ServiceOperationsResult[response_model] = await self._service_operations.read(
            selector=body, response_model=response_model
        )
        return self._raise_errors(service_operations_result)

    async def update(
            self,
            body: _RequestTypeT,
            response_model: _ResponseTypeT
    ) -> ServiceOperationsSuccess[_ResponseTypeT]:
        service_operations_result: ServiceOperationsResult[response_model] = await self._service_operations.update(
                request=body, response_model=response_model
        )
        return self._raise_errors(service_operations_result)

    async def delete(
            self,
            body: _RequestTypeT,
            response_model: _ResponseTypeT
    ) -> ServiceOperationsSuccess[_ResponseTypeT]:
        service_operations_result: ServiceOperationsResult[response_model] = await self._service_operations.delete(
                request=body, response_model=response_model
        )
        return self._raise_errors(service_operations_result)

    @classmethod
    def _raise_errors(
            cls,
            service_operations_result: ServiceOperationsResult[_ResponseTypeT]
    ) -> ServiceOperationsSuccess[_ResponseTypeT]:
        if service_operations_result.name == 'service-error':
            raise HTTPException(
                status_code=ExceptionMappingUtil.get_exception_code(service_operations_result.error_type),
                detail=ExceptionMappingUtil.get_exception_message(service_operations_result.error_type)
            )
        return service_operations_result