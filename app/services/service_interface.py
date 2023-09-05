"""Abstraction of application services, every service needs to implement this"""
from abc import abstractmethod

from functools import wraps

from typing import TypeVar, TypeAlias, Literal, Generic, Union, Callable, Any

from pydantic import BaseModel as BaseModelPydantic

from sqlalchemy.exc import SQLAlchemyError

from app.utils import ExceptionType, ExceptionMappingUtil

# generics
T = TypeVar('T')
_SchemaTypeT = TypeVar('_SchemaTypeT')
_ModelTypeT = TypeVar('_ModelTypeT')

# types
ResultNameLiteral: TypeAlias = Literal['service-success', 'service-error']


class ServiceOperationsError(BaseModelPydantic):
    name: ResultNameLiteral = 'service-error'
    error_type: ExceptionType


class ServiceOperationsSuccess(Generic[T], BaseModelPydantic):
    name: ResultNameLiteral = 'service-success'
    data: T


ServiceOperationsResult: Union[T] = ServiceOperationsError | ServiceOperationsSuccess[T]


# decorators
def mappedresult(func) -> Callable:
    @wraps(func)
    async def wrapper_function(*args, **kwargs) -> ServiceOperationsResult[_SchemaTypeT]:
        try:
            response_model: _SchemaTypeT = kwargs['response_model']
            response: response_model = await func(*args, **kwargs)
            return ServiceOperationsSuccess(**{
                'data': response
            })
        except SQLAlchemyError as exc:
            return ServiceOperationsError(**{
                'error_type': ExceptionMappingUtil.get_exception_type(exc),
            })
    return wrapper_function


class ServiceInterface:
    @abstractmethod
    async def create(
            self,
            response_model: Generic[_SchemaTypeT],
            request: BaseModelPydantic
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass

    @abstractmethod
    async def read(
            self,
            response_model: Generic[_SchemaTypeT],
            selector: Any
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass

    @abstractmethod
    async def update(
            self,
            response_model: Generic[_SchemaTypeT],
            request: BaseModelPydantic
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass

    @abstractmethod
    async def delete(
            self,
            response_model: Generic[_SchemaTypeT],
            request: BaseModelPydantic
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass
