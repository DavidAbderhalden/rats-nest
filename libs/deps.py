from libs.services.database_operations import DatabaseOperationsService
from functools import lru_cache

# Used for dependency injections

@lru_cache
def get_database_operations_service() -> DatabaseOperationsService:
    return DatabaseOperationsService()