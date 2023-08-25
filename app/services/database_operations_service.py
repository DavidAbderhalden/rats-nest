"""Service used for all database related operations"""
from typing import Callable

from contextlib import AbstractContextManager, contextmanager

from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.engine import URL, Engine, create_engine

from app.environments.settings import settings as app_settings
from app.schemas import PostAccountsRegisterSchema

class DatabaseOperationsService:
    _source_uri: URL
    _engine: Engine
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
            username=app_settings.DATABASE_USER,
            password=app_settings.DATABASE_PASSWORD,
            host=app_settings.DATABASE_HOST,
            port=app_settings.DATABASE_PORT,
            database=app_settings.DATABASE_NAME
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

    # TODO: Implement
    def create_customer(self, customer_data: PostAccountsRegisterSchema) -> bool:
        pass

    # TODO: Implement
    def modify_customer(self):
        pass

    # TODO: Implement
    def delete_customer(self):
        pass

    def get_engine(self) -> Engine:
        return self._engine

    def get_source_uri(self) -> URL:
        return self._source_uri

databaseOperationsService = DatabaseOperationsService()
