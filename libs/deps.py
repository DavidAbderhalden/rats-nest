from libs.services.database_operations import DatabaseOperationsService
from libs.environments.settings import Base
from functools import lru_cache

# Used for dependency injections

@lru_cache
def get_database_operations_service() -> DatabaseOperationsService:
    return DatabaseOperationsService()

@lru_cache
def get_app_settings() -> Base:
    return Base()