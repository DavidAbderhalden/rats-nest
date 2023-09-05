from abc import abstractmethod

from traceback import format_exception

from functools import wraps

from typing import TypeVar, TypeAlias, Literal, Generic, Union, Callable

from pydantic import BaseModel as BaseModelPydantic

# generics
T = TypeVar('T')
_SchemaTypeT = TypeVar('_SchemaTypeT')
_ModelTypeT = TypeVar('_ModelTypeT')

# types
ResultNameLiteral: TypeAlias = Literal['service-success', 'service-error']


class ServiceOperationsError(BaseModelPydantic):
    name: ResultNameLiteral = 'service-error'
    error: str


class ServiceOperationsSuccess(Generic[T], BaseModelPydantic):
    name: ResultNameLiteral = 'service-success'
    data: T


ServiceOperationsResult: Union[T] = ServiceOperationsError | ServiceOperationsSuccess[T]


# decorators
def mappedresult(func) -> Callable:
    @wraps(func)
    async def wrapper_function(*args, **kwargs) -> ServiceOperationsResult[_SchemaTypeT]:
        try:
            _ResponseModel: _SchemaTypeT = kwargs['response_model']
            response: _ResponseModel = await func(*args, **kwargs)
            return ServiceOperationsSuccess(**{
                'data': response
            })
        except Exception as exc:
            return ServiceOperationsError(**{
                'error': ''.join(format_exception(exc)),
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
            self, response_model: Generic[_SchemaTypeT]
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
