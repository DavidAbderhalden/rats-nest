"""Base schema for pydantic models"""
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder

class BaseSchema(BaseModel):

    def get_json(self) -> dict:
        return jsonable_encoder(self)
