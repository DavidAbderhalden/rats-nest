"""Service responsible for creating authentications"""
from typing import Generic, Any, TypeVar

from uuid import uuid4

from pydantic import BaseModel as BaseModelPydantic
from starlette.background import BackgroundTasks
from starlette.requests import Request

from app.schemas import IdentificationCreate, AuthenticationsCreate
from app.models import CustomersModel, AuthenticationsModel
from app.repository import database_operations_service
from app.utils import CryptographyUtil
from app.exceptions.libs import NoClientHostError, UnverifiedEmailError, AuthenticationError, InvalidRefreshToken, RefreshError
from .. import TokenPayload, jwt_service, authorization_service
from ..authorization_service import AuthenticationRequestPayload
from ..service_interface import ServiceOperationsResult, ServiceInterface, mappedresult

# generics
_SchemaTypeT = TypeVar('_SchemaTypeT')


class AuthenticationService(ServiceInterface):
    @mappedresult
    async def create(
            self,
            response_model: Generic[_SchemaTypeT],
            request: IdentificationCreate,
            background_task: BackgroundTasks
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        # FIXME: Old entries should be deleted from time to time
        value: str = request.email if request.email else request.username
        attribute_name: str = 'primary_email' if request.email else 'username'
        active_customer: CustomersModel = await database_operations_service.get_by_attribute_or_throw(
            value=value, attr_name=attribute_name, model_type=CustomersModel
        )
        if not request.client_host:
            raise NoClientHostError()

        identity_verified: bool = CryptographyUtil.validate_password(
            plain_text_password=bytes(request.password, 'utf8'), password_hash=bytes(active_customer.password, 'utf8')
        )
        if not identity_verified:
            raise AuthenticationError()

        is_customer_email_verified: bool = await database_operations_service.is_customer_verified(active_customer.id)
        if not is_customer_email_verified:
            raise UnverifiedEmailError(active_customer.primary_email)

        await database_operations_service.delete_by_attribute_if_exists(
            value=active_customer.id, attr_name='customer_id', model_type=AuthenticationsModel
        )
        return await database_operations_service.create(AuthenticationsCreate(
            host_name=request.client_host, customer_id=active_customer.id, auth_token=str(uuid4())
        ), AuthenticationsModel)

    @mappedresult
    async def read(
            self,
            response_model: Generic[_SchemaTypeT],
            selector: AuthenticationRequestPayload
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        return await database_operations_service.get_by_attribute_or_throw(
            value=selector.customer_id, attr_name='customer_id', model_type=AuthenticationsModel
        )

    @mappedresult
    async def update(
            self,
            response_model: Generic[_SchemaTypeT],
            request: Request
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        refresh_token: str = authorization_service.get_refresh_token_from_request(request)
        token_payload: TokenPayload | None = jwt_service.validate_token(refresh_token)
        if not token_payload:
            raise InvalidRefreshToken()
        active_customer: CustomersModel | None = await authorization_service.get_validated_customer_from_auth_token(
            auth_token=token_payload.auth_token, host_name=request.client.host
        )
        if not active_customer:
            raise RefreshError()

        return await database_operations_service.get_or_create(AuthenticationsCreate(
            host_name=request.client.host, customer_id=active_customer.id, auth_token=token_payload.auth_token
        ), AuthenticationsModel)

    @mappedresult
    async def delete(
            self,
            response_model: Generic[_SchemaTypeT],
            request: AuthenticationRequestPayload
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        await database_operations_service.delete_by_attribute_if_exists(
            value=request.customer_id, attr_name='customer_id', model_type=AuthenticationsModel
        )
        return 'ok'
