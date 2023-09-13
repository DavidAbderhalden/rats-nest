"""Service that handles all operations on verification codes"""
from typing import Generic, Any, TypeVar

from base64 import urlsafe_b64decode

from pydantic import BaseModel as BaseModelPydantic
from starlette.background import BackgroundTasks

from app.models import ConfirmationCodesModel
from app.repository import database_operations_service
from app.schemas import ConfirmationCodesUpdate
from .. import ServiceOperationsResult
from ..service_interface import ServiceInterface, mappedresult

# generics
_SchemaTypeT = TypeVar('_SchemaTypeT')


class VerificationService(ServiceInterface):
    @mappedresult
    async def create(
            self,
            response_model: Generic[_SchemaTypeT],
            request: BaseModelPydantic,
            background_task: BackgroundTasks
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass

    @mappedresult
    async def read(
            self,
            response_model: Generic[_SchemaTypeT],
            selector: Any
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass

    @mappedresult
    async def update(
            self,
            response_model: Generic[_SchemaTypeT],
            request: ConfirmationCodesUpdate
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        reconstructed_codes: ConfirmationCodesUpdate = ConfirmationCodesUpdate(
            email_validation=urlsafe_b64decode(
                bytes(request.email_validation, 'ascii')).decode('utf8') if request.email_validation else None,
            password_reset=urlsafe_b64decode(
                bytes(request.password_reset, 'ascii')).decode('utf8') if request.password_reset else None
        )
        return await database_operations_service.delete_attributes_or_throw(
            entity=reconstructed_codes, model_type=ConfirmationCodesModel
        )

    @mappedresult
    async def delete(
            self,
            response_model: Generic[_SchemaTypeT],
            request: BaseModelPydantic
    ) -> ServiceOperationsResult[_SchemaTypeT]:
        pass
