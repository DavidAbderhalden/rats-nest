from fastapi import Request
from fastapi.exceptions import HTTPException
from starlette.types import Scope

import inspect

from app.schemas import BaseSchema
from app.models import Roles, CustomersModel, AuthenticationsModel
from app.repository import database_operations_service
from .jwt_service import jwt_service, TokenPayload


class AuthenticationRequestPayload(BaseSchema):
    role: Roles
    customer_id: int
    host_name: str
    access_token: str
    refresh_token: str


class AuthenticatedRequest(Request):
    auth_body: AuthenticationRequestPayload

    def __init__(self, scope: Scope, auth_body: AuthenticationRequestPayload):
        super().__init__(scope)
        self.auth_body = auth_body


def auth_required(role: Roles = Roles.USER):
    def decorator(function):
        async def wrapper(req: Request, *args, **kwargs):
            authenticated_request: AuthenticationRequestPayload | None = await authorization_service.verify_authentication(req)
            if not authenticated_request or not authenticated_request.role.superior_or_equal(role):
                raise HTTPException(
                    status_code=403,
                    detail='Unauthorized request'
                )
            authenticated_request: AuthenticatedRequest = AuthenticatedRequest(scope=req.scope, auth_body=authenticated_request)
            return await function(request=authenticated_request, *args, **kwargs)

        wrapper.__signature__ = inspect.Signature(
            parameters=[
                *inspect.signature(function).parameters.values(),
                *filter(
                    lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                    inspect.signature(wrapper).parameters.values()
                )
            ],
            return_annotation=inspect.signature(function).return_annotation,
        )
        return wrapper
    return decorator


class AuthorizationService:
    async def verify_authentication(self, request: Request) -> AuthenticationRequestPayload | None:
        access_token: str = self.get_access_token_from_request(request)
        refresh_token: str = self.get_refresh_token_from_request(request)
        access_token_payload: TokenPayload | None = jwt_service.validate_token(access_token)
        refresh_token_payload: TokenPayload | None = jwt_service.validate_token(refresh_token)
        if not access_token_payload or not refresh_token_payload:
            return
        active_customer: CustomersModel | None = await self.get_validated_customer_from_auth_token(
            auth_token=access_token_payload.auth_token, host_name=request.client.host)
        if not active_customer:
            return
        return AuthenticationRequestPayload(
            role=active_customer.role,
            customer_id=active_customer.id,
            host_name=request.client.host,
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def get_validated_customer_from_auth_token(self, auth_token: str, host_name: str) -> CustomersModel | None:
        customer_authentication: AuthenticationsModel | None = await database_operations_service.get_by_attribute_or_none(
            auth_token, 'auth_token', AuthenticationsModel
        )
        if not customer_authentication:
            return
        customer_id: int = customer_authentication.customer_id
        authenticated_host: str = customer_authentication.host_name
        if not authenticated_host == host_name:
            return
        return await database_operations_service.get_by_id(customer_id, model_type=CustomersModel)

    def get_access_token_from_request(self, request: Request) -> str:
        try:
            return request.headers.get('Authorization').split('Bearer ')[-1].strip()
        except AttributeError:
            return ''

    def get_refresh_token_from_request(self, request: Request) -> str:
        try:
            return request.cookies.get('refreshToken').strip()
        except AttributeError:
            return ''


authorization_service: AuthorizationService = AuthorizationService()