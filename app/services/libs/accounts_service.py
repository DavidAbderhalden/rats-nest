from typing import Generic, TypeVar

from pydantic import BaseModel as BaseModelPydantic

from ..service_interface import ServiceInterface, ServiceOperationsResult, mappedresult

from app.schemas.glue import CustomersGlue, AddressGlue
from app.schemas import StreetsCreate, AddressCreate, CustomersCreate
from app.models import CitiesModel, StreetsModel, CustomersModel, AddressModel
from app.repository import database_operations_service
from app.utils import CryptographyUtil

# generics
_SchemaTypeT = TypeVar('_SchemaTypeT')
_ModelTypeT = TypeVar('_ModelTypeT')


# TODO: Implement
class AccountsService(ServiceInterface):
    @mappedresult
    async def create(
            self,
            response_model: Generic[_SchemaTypeT],
            request: CustomersGlue
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        home_address_id: int = await AccountsService._get_address_id(request.home_address)
        delivery_address_id: int = await AccountsService._get_address_id(request.delivery_address)
        hashed_password: bytes = CryptographyUtil.salty_hash(bytes(request.password, encoding='utf-8'))
        return await database_operations_service.create(
            entity=CustomersCreate(**{
                **request.get_json(),
                'password': hashed_password,
                'delivery_address_id': delivery_address_id,
                'home_address_id': home_address_id
            }),
            model_type=CustomersModel
        )

    @mappedresult
    async def read(
            self,
            response_model: Generic[_SchemaTypeT]
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

    @classmethod
    async def _get_address_id(cls, address: AddressGlue) -> int:
        city: CitiesModel = await database_operations_service.get_or_create(
            entity=address.street.city,
            model_type=CitiesModel
        )
        street: StreetsModel = await database_operations_service.get_or_create(
            entity=StreetsCreate(**{
                'name': address.street.name,
                'city_id': city.id
            }),
            model_type=StreetsModel
        )

        address: AddressModel = await database_operations_service.get_or_create(
            entity=AddressCreate(**{
                'house_number': address.house_number,
                'street_id': street.id
            }),
            model_type=AddressModel
        )
        return address.id
