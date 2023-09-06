"""Service used to handle all address related actions"""
from typing import Generic, TypeVar

from pydantic import BaseModel as BaseModelPydantic

from fuzzywuzzy import fuzz

from app.repository import database_operations_service
from app.schemas.glue import AddressGlueRead, AddressGlueCreate
from app.schemas import StreetsCreate, AddressCreate, AddressRead, CitiesRead, StreetsRead
from app.models import CitiesModel, StreetsModel, AddressModel
from ..service_interface import ServiceInterface, ServiceOperationsResult, mappedresult

# generics
_SchemaTypeT = TypeVar('_SchemaTypeT')

class SearchAddressQueryParams(BaseModelPydantic):
    address: str
    limit: int


class AddressService(ServiceInterface):
    @mappedresult
    async def create(
            self,
            response_model: Generic[_SchemaTypeT],
            request: AddressGlueCreate
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        return await AddressService.get_or_create_address(request)

    @mappedresult
    async def update(self, response_model: Generic[_SchemaTypeT], request: BaseModelPydantic) -> \
    ServiceOperationsResult[_SchemaTypeT]:
        pass

    @mappedresult
    async def delete(self, response_model: Generic[_SchemaTypeT], request: BaseModelPydantic) -> \
    ServiceOperationsResult[_SchemaTypeT]:
        pass

    @mappedresult
    async def read(
            self,
            response_model: Generic[_SchemaTypeT],
            selector: SearchAddressQueryParams
    ) -> ServiceOperationsResult[_SchemaTypeT]:

        address_strings: list[str] = await database_operations_service.get_address_strings()

        def is_string_similar(element: str, MIN_SIMILARITY_PERCENTAGE: int = 80) -> bool:
            return fuzz.WRatio(element, selector.address) >= MIN_SIMILARITY_PERCENTAGE

        fuzzy_address_strings: list[str] = sorted(
            (address for address in address_strings if is_string_similar(address)),
            key=is_string_similar
        )
        print(fuzzy_address_strings)
        return fuzzy_address_strings[:selector.limit]

    @classmethod
    async def get_or_create_address(cls, address_glue: AddressGlueCreate) -> AddressGlueRead:
        city: CitiesModel = await database_operations_service.get_or_create(
            entity=address_glue.street.city,
            model_type=CitiesModel
        )
        street: StreetsModel = await database_operations_service.get_or_create(
            entity=StreetsCreate(**{
                'name': address_glue.street.name,
                'city_id': city.id
            }),
            model_type=StreetsModel
        )
        address: AddressModel = await database_operations_service.get_or_create(
            entity=AddressCreate(**{
                'house_number': address_glue.house_number,
                'street_id': street.id
            }),
            model_type=AddressModel
        )
        return AddressGlueRead(**{
            **AddressRead.model_validate(address).get_json(),
            'street': {
                **StreetsRead.model_validate(street).get_json(),
                'city': {
                    **CitiesRead.model_validate(city).get_json()
                }
            }
        })