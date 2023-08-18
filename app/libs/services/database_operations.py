from sqlalchemy import Engine, create_engine, QueuePool
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from app.libs.environments.settings import Settings
from functools import lru_cache
from typing import Iterator

class DatabaseOperationsService:
    _engine: Engine
    _settings: Settings = Settings()
    # _SessionLocal: sessionmaker
    BaseModel = declarative_base()

    def __init__(self) -> None:
        source_uri: URL = DatabaseOperationsService._create_source_uri()
        self._engine = create_engine(source_uri, pool_pre_ping=True, pool_recycle=90, pool_size=10, poolclass=QueuePool)
        # self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        self._init_tables()

    @classmethod
    def _create_source_uri(cls) -> URL:
        return URL.create(
            drivername='mysql',
            username='root',
            password='root',
            host='127.0.0.1',
            port=3306,
            database='gekko'
        )

    def get_session(self) -> Iterator[Session]:
        with Session(self._engine) as session:
            yield session

    def _init_tables(self) -> None:
        DatabaseOperationsService.BaseModel.metadata.create_all(bind=self._engine)

@lru_cache
def get_database_operations_service() -> DatabaseOperationsService:
    return DatabaseOperationsService()
