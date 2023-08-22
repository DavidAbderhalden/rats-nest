"""Service used for all database related operations"""
from typing import Callable

from contextlib import AbstractContextManager, contextmanager

from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.engine import URL, Engine, create_engine

from app.environments.settings import Settings

class DatabaseOperationsService:
    _source_uri: URL
    _engine: Engine
    _settings: Settings = Settings()
    _session_factory: scoped_session

    def __init__(self) -> None:
        self._source_uri: URL = self._create_source_uri()
        self._engine = \
            create_engine(self._source_uri, pool_pre_ping=True, pool_recycle=90, pool_size=10, poolclass=QueuePool)
        self._session_factory = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))

    @classmethod
    def _create_source_uri(cls) -> URL:
        return URL.create(
            drivername='mysql+mariadbconnector',
            username=DatabaseOperationsService._settings.DATABASE_USER,
            password=DatabaseOperationsService._settings.DATABASE_PASSWORD,
            host=DatabaseOperationsService._settings.DATABASE_HOST,
            port=DatabaseOperationsService._settings.DATABASE_PORT,
            database=DatabaseOperationsService._settings.DATABASE_NAME
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_engine(self) -> Engine:
        return self._engine

    def get_source_uri(self) -> URL:
        return self._source_uri

databaseOperationsService = DatabaseOperationsService()
