from fastapi import APIRouter

from typing import Type

from app.schemas import CustomersRead, CitiesCreate, StreetsCreate, AddressCreate, CustomersCreate
from app.schemas.glue import CustomersGlue, AddressGlue

from app.models import CustomersModel, CitiesModel, StreetsModel, AddressModel

from app.controller.base_controller import BaseController

from app.utils import CryptographyUtil

accounts_controller: APIRouter = APIRouter(prefix='/accounts')
base_controller: BaseController = BaseController(provider_name='accounts-controller')


@accounts_controller.post('/register', response_model=CustomersRead)
async def register(body: CustomersGlue):
    home_address_entry: AddressModel = await get_or_create_address(body.home_address)
    delivery_address_entry: AddressModel = await get_or_create_address(body.delivery_address)
    customers_template: CustomersCreate = CustomersCreate(**{
        **body.get_json(),
        'password': CryptographyUtil.salty_hash(bytes(body.password, encoding='utf-8')),
        'delivery_address_id': delivery_address_entry.id,
        'home_address_id': home_address_entry.id
    })
    return await base_controller.create(customers_template, CustomersModel)


async def get_or_create_address(address: AddressGlue) -> AddressModel:
    city_template: CitiesCreate = address.street.city
    city_tuple: Type[CitiesModel] = await base_controller.create(city_template, CitiesModel, get_if_existing=True)
    street_template: StreetsCreate = StreetsCreate(**{
        'name': address.street.name,
        'city_id': city_tuple.id
    })
    street_tuple: Type[StreetsModel] = await base_controller.create(street_template, StreetsModel, get_if_existing=True)
    address_template: AddressCreate = AddressCreate(**{
        'house_number': address.house_number,
        'street_id': street_tuple.id
    })
    return await base_controller.create(address_template, AddressModel, get_if_existing=True)
