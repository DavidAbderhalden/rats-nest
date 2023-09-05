"""Service for handling all account related actions"""
from typing import Generic, TypeVar

from pydantic import BaseModel as BaseModelPydantic

from app.schemas.glue import CustomersGlueCreate, AddressGlueRead, CustomersGlueRead
from app.schemas import CustomersCreate, CustomersRead
from app.models import CustomersModel
from app.repository import database_operations_service
from app.utils import CryptographyUtil
from .address_service import AddressService
from ..service_interface import ServiceInterface, ServiceOperationsResult, mappedresult

# generics
_SchemaTypeT = TypeVar('_SchemaTypeT')
_ModelTypeT = TypeVar('_ModelTypeT')


class AccountsService(ServiceInterface):
    @mappedresult
    async def create(
            self,
            response_model: Generic[_SchemaTypeT],
            request: CustomersGlueCreate
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        home_address: AddressGlueRead = await AddressService.get_or_create_address(request.home_address)
        delivery_address: AddressGlueRead = await AddressService.get_or_create_address(request.delivery_address)
        hashed_password: bytes = CryptographyUtil.salty_hash(bytes(request.password, encoding='utf-8'))
        customer: CustomersModel = await database_operations_service.create(
            entity=CustomersCreate(**{
                **request.get_json(),
                'password': hashed_password,
                'delivery_address_id': home_address.id,
                'home_address_id': delivery_address.id
            }),
            model_type=CustomersModel
        )
        return CustomersGlueRead(**{
            **CustomersRead.model_validate(customer).get_json(),
            'home_address': {
                **AddressGlueRead.model_validate(home_address).get_json()
            },
            'delivery_address': {
                **AddressGlueRead.model_validate(delivery_address).get_json()
            }
        })

    @mappedresult
    async def read(
            self,
            response_model: Generic[_SchemaTypeT],
            selector: int
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass

    @mappedresult
    async def update(
            self,
            response_model: Generic[_SchemaTypeT],
            request: BaseModelPydantic
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass

    @mappedresult
    async def delete(
            self,
            response_model: Generic[_SchemaTypeT],
            request: BaseModelPydantic
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass
