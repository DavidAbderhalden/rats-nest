from fastapi import APIRouter

from typing import Type

from app.schemas import CustomersRead, CitiesCreate, StreetsCreate, AddressCreate, CustomersCreate
from app.schemas.glue import CustomersGlue, AddressGlue
from app.models import CustomersModel, CitiesModel, StreetsModel, AddressModel
from app.controller.base_controller import BaseController


accounts_controller: APIRouter = APIRouter(prefix='/accounts')
base_controller: BaseController = BaseController(provider_name='accounts-controller')

@accounts_controller.post('/register', response_model=CustomersRead)
async def register(body: CustomersGlue):
    home_address_entry: AddressModel = get_or_create_address(body.home_address)
    delivery_address_entry: AddressModel = get_or_create_address(body.delivery_address)
    customers_template: CustomersCreate = CustomersCreate(**{
        **body.get_json(),
        'delivery_address_id': delivery_address_entry.id,
        'home_address_id': home_address_entry.id
    })
    # FIXME: Security issue!
    # TODO: Not create if exists and return wrong customer probably, check if already exists ...
    return base_controller.create(customers_template, CustomersModel)

def get_or_create_address(address: AddressGlue) -> AddressModel:
    city_template: CitiesCreate = address.street.city
    city_tuple: Type[CitiesModel] = base_controller.create(city_template, CitiesModel, get_if_existing=True)
    street_template: StreetsCreate = StreetsCreate(**{
        'name': address.street.name,
        'city_id': city_tuple.id
    })
    street_tuple: Type[StreetsModel] = base_controller.create(street_template, StreetsModel, get_if_existing=True)
    address_template: AddressCreate = AddressCreate(**{
        'house_number': address.house_number,
        'street_id': street_tuple.id
    })
    return base_controller.create(address_template, AddressModel, get_if_existing=True)
