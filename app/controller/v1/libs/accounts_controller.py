from fastapi import APIRouter

from typing import Type

from app.schemas import CustomersRead
from app.schemas.glue import CustomersGlue
from app.controller.base_controller import BaseController
from app.services.libs import AccountsService
from app.services import ServiceOperationsSuccess

accounts_controller: APIRouter = APIRouter(prefix='/accounts')

base_controller: BaseController = BaseController(service_operations=AccountsService(), provider_name='account-service')


@accounts_controller.post('/register', response_model=CustomersRead)
async def register(body: CustomersGlue):
    service_success: ServiceOperationsSuccess[Type[CustomersRead]] = \
        await base_controller.create(body, response_model=CustomersRead)
    return service_success.data
