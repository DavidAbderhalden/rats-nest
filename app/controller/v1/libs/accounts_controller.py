from fastapi import APIRouter, BackgroundTasks

from typing import Type

from app.schemas.glue import CustomersGlueCreate, CustomersGlueRead
from app.controller.base_controller import BaseController
from app.services.libs import AccountsService
from app.services import ServiceOperationsSuccess

accounts_controller: APIRouter = APIRouter(prefix='/accounts')

base_controller: BaseController = BaseController(service_operations=AccountsService(), provider_name='account-service')


@accounts_controller.post('/register', response_model=CustomersGlueRead)
async def register(body: CustomersGlueCreate, background_task: BackgroundTasks):
    service_success: ServiceOperationsSuccess[Type[CustomersGlueRead]] = await base_controller.create(
        body=body, response_model=CustomersGlueRead, background_task=background_task
    )
    return service_success.data
