from typing import Type

from fastapi import APIRouter, Request, Response

from app.schemas import IdentificationCreate, AuthenticationsRead
from app.controller.base_controller import BaseController
from app.services.libs import AuthenticationService
from app.services import (ServiceOperationsSuccess, jwt_service, TokenPayload, auth_required, AuthenticatedRequest)
from services.authorization_service import AuthenticationRequestPayload

authentication_controller = APIRouter(prefix='/auth')

base_controller = BaseController(
    service_operations=AuthenticationService(),
    provider_name='authentication-service'
)


@authentication_controller.post('/token', response_model=AuthenticationsRead)
async def login(
        body: IdentificationCreate,
        request: Request,
        response: Response
    ):
    body.client_host = request.client.host
    service_success: ServiceOperationsSuccess[Type[AuthenticationsRead]] = await base_controller.create(
        body=body, response_model=AuthenticationsRead
    )
    access_token: str = jwt_service.generate_access_token(data=TokenPayload(auth_token=service_success.data.auth_token))
    refresh_token: str = jwt_service.generate_refresh_token(data=TokenPayload(auth_token=service_success.data.auth_token))
    response.set_cookie(
        key='accessToken',
        value=access_token,
        max_age=jwt_service.get_access_token_validity_delta_seconds(),
        expires=jwt_service.get_token_expiration_date(access_token),
        httponly=False,
        samesite='strict',
        secure=False # Should be true in prod
    )
    response.set_cookie(
        key='refreshToken',
        value=refresh_token,
        max_age=jwt_service.get_refresh_token_validity_delta_seconds(),
        expires=jwt_service.get_token_expiration_date(refresh_token),
        httponly=True,
        samesite='strict',
        secure=False # Should be true in prod
    )
    return service_success.data

@authentication_controller.get('/refresh', response_model=AuthenticationsRead)
async def refresh(request: Request, response: Response):
    service_success: ServiceOperationsSuccess[Type[AuthenticationsRead]] = await base_controller.update(
        body=request, response_model=AuthenticationsRead
    )
    access_token: str = jwt_service.generate_access_token(data=TokenPayload(auth_token=service_success.data.auth_token))
    refresh_token: str = jwt_service.generate_refresh_token(data=TokenPayload(auth_token=service_success.data.auth_token))
    response.set_cookie(
        key='accessToken',
        value=access_token,
        max_age=jwt_service.get_access_token_validity_delta_seconds(),
        expires=jwt_service.get_token_expiration_date(access_token),
        httponly=False,
        samesite='strict',
        secure=False # Should be true in prod
    )
    response.set_cookie(
        key='refreshToken',
        value=refresh_token,
        max_age=jwt_service.get_refresh_token_validity_delta_seconds(),
        expires=jwt_service.get_token_expiration_date(refresh_token),
        httponly=True,
        samesite='strict',
        secure=False # Should be true in prod
    )
    return service_success.data

@authentication_controller.get('/verify', response_model=AuthenticationsRead)
@auth_required()
async def verify(request: AuthenticatedRequest):
    service_success: ServiceOperationsSuccess[Type[AuthenticationsRead]] = await base_controller.read(
        body=request.auth_body, response_model=AuthenticationsRead
    )
    return service_success.data

@authentication_controller.post('/logout')
@auth_required()
async def logout(request: AuthenticatedRequest, response: Response):
    service_success: ServiceOperationsSuccess[Type[str]] = await base_controller.delete(
        body=request.auth_body, response_model=str
    )
    response.delete_cookie('accessToken')
    response.delete_cookie('refreshToken')
    return service_success.data
