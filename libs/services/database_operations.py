from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from libs.environments.settings import Base
from functools import lru_cache

class DatabaseOperationsService:
    _engine: Engine
    _settings: Base = Base()
    _SessionLocal: sessionmaker
    Base: declarative_base = declarative_base()

    def __init__(self) -> None:
        source_uri: str = DatabaseOperationsService._create_source_uri()
        self._engine = create_engine(source_uri)
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @classmethod
    def _create_source_uri(cls) -> str:
        return (
            f'mysql+pymysql://'
            f'{DatabaseOperationsService._settings.DATABASE_USER}:'
            f'{DatabaseOperationsService._settings.DATABASE_PASSWORD}@'
            f'{DatabaseOperationsService._settings.DATABASE_HOST}:'
            f'{DatabaseOperationsService._settings.DATABASE_PORT}/'
            f'{DatabaseOperationsService._settings.DATABASE_NAME}'
            f'?charset=utf8mb4'
        )

@lru_cache
def get_database_operations_service() -> DatabaseOperationsService:
    return DatabaseOperationsService()

BaseModel = declarative_base()

# Models can be defined here