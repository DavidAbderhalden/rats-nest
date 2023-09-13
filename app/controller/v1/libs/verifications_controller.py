from typing import Type

from fastapi import APIRouter

from app.controller.base_controller import BaseController
from app.services.libs import VerificationService
from app.services import ServiceOperationsSuccess
from app.schemas import ConfirmationCodesUpdate, ConfirmationCodesRead

verifications_controller = APIRouter(prefix='/verify')

base_controller = BaseController(service_operations=VerificationService(), provider_name='verification-service')


@verifications_controller.patch('/codes', response_model=ConfirmationCodesRead)
async def verify_codes(body: ConfirmationCodesUpdate):
    service_success: ServiceOperationsSuccess[Type[ConfirmationCodesRead]] = await base_controller.update(
        body=body, response_model=ConfirmationCodesRead
    )
    return service_success.data