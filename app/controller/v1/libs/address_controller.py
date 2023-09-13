from fastapi import APIRouter

from typing import Type

from app.controller.base_controller import BaseController
from app.services.libs import AddressService, SearchAddressQueryParams
from app.services import ServiceOperationsSuccess
from app.schemas.glue import AddressGlueCreate, AddressGlueRead

address_controller = APIRouter(prefix='/address')

base_controller: BaseController = BaseController(service_operations=AddressService(), provider_name='address-service')


@address_controller.get('/search', response_model=list[str])
async def search_address(addr: str, limit: int = 20):
    service_success: ServiceOperationsSuccess[Type[list[str]]] = await base_controller.read(
        body=SearchAddressQueryParams(address=addr, limit=limit), response_model=list[str]
    )
    return service_success.data


@address_controller.post('/create', response_model=AddressGlueRead)
async def create_address(body: AddressGlueCreate):
    service_success: ServiceOperationsSuccess[Type[AddressGlueRead]] = await base_controller.create(
        body=body, response_model=AddressGlueRead
    )
    return service_success.data
