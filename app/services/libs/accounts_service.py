"""Service for handling all account related actions"""
from typing import Generic, TypeVar

from pydantic import BaseModel as BaseModelPydantic

from fastapi import BackgroundTasks

from fastapi_mail import MessageSchema

from app.schemas.glue import CustomersGlueCreate, AddressGlueRead, CustomersGlueRead
from app.schemas import CustomersCreate, CustomersRead, ConfirmationCodesCreate
from app.models import CustomersModel, ConfirmationCodesModel
from app.repository import database_operations_service
from app.utils import CryptographyUtil, StringTransformationUtil
from .address_service import AddressService
from ..email_service import emailService
from ..service_interface import ServiceInterface, ServiceOperationsResult, mappedresult

# generics
_SchemaTypeT = TypeVar('_SchemaTypeT')
_ModelTypeT = TypeVar('_ModelTypeT')


class AccountsService(ServiceInterface):
    @mappedresult
    async def create(
            self,
            response_model: Generic[_SchemaTypeT],
            request: CustomersGlueCreate,
            background_task: BackgroundTasks,
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
        email_validation_code: str = await AccountsService._create_email_validation_code(customer.id)
        # do I want to send the email to both addresses?
        verification_mail: MessageSchema = emailService.create_email_verification_mail(
            recipients=[customer.primary_email],
            verification_code=email_validation_code,
            username=customer.username
        )
        emailService.send(background_task=background_task, message=verification_mail)
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

    @classmethod
    async def _create_email_validation_code(cls, customer_id: int) -> str:
        random_code: str = StringTransformationUtil.create_random_code(
            length=20, upper_case=True, lower_case=True, digits=True, specials=True
        )
        confirmation_codes_create: ConfirmationCodesCreate = ConfirmationCodesCreate(**{
            'email_validation': random_code,
            'customer_id': customer_id
        })
        confirmation_codes: ConfirmationCodesModel = await database_operations_service.create(
            confirmation_codes_create, model_type=ConfirmationCodesModel
        )
        return confirmation_codes.email_validation
