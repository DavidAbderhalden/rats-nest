"""Service used for all database related operations"""
from traceback import format_exception

from functools import wraps

from typing import Callable, Literal, TypeVar, TypeAlias, Generic, Union

from contextlib import AbstractContextManager, contextmanager

from pydantic import BaseModel as BaseModelPydantic

from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import URL, Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.environments.settings import settings as app_settings
from app.schemas import BaseSchema

# generics
T = TypeVar('T')
_ModelTypeT = TypeVar('_ModelTypeT')

ResultNameLiteral: TypeAlias = Literal['database-success', 'database-error']

# decorators
def exception_handled(func) -> Callable:
    @wraps(func)
    def wrapper_function(*args, **kwargs) -> DatabaseOperationsResult[_ModelTypeT]:
        try:
            _model_type: _ModelTypeT = kwargs['_model_type']
            new_tuple: _model_type = func(*args, **kwargs)
            return DatabaseOperationsSuccess(**{
                'data': new_tuple
            })
        except SQLAlchemyError as db_exception:
            return DatabaseOperationsError(**{
                'error': ''.join(format_exception(db_exception))
            })
    return wrapper_function

class DatabaseOperationsError(BaseModelPydantic):
    name: ResultNameLiteral = 'database-error'
    error: str

class DatabaseOperationsSuccess(Generic[T], BaseModelPydantic):
    name: ResultNameLiteral = 'database-success'
    data: T

DatabaseOperationsResult: Union[T] = DatabaseOperationsError | DatabaseOperationsSuccess[T]

# TODO: Make async?
# TODO: Create email etc verification tables
class DatabaseOperationsService:
    _source_uri: URL
    _engine: Engine
    _session_factory: sessionmaker

    def __init__(self) -> None:
        self._source_uri: URL = self._create_source_uri()
        self._engine = create_engine(
            self._source_uri,
            pool_pre_ping=True,
            pool_recycle=90,
            pool_size=10,
            poolclass=QueuePool
        )
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=self._engine,
            expire_on_commit=False
        )

    @classmethod
    def _create_source_uri(cls) -> URL:
        return URL.create(
            drivername='mysql+mysqlconnector',
            username=app_settings.DATABASE_USER,
            password=app_settings.DATABASE_PASSWORD,
            host=app_settings.DATABASE_HOST,
            port=app_settings.DATABASE_PORT,
            database=app_settings.DATABASE_NAME,
            query={'charset': 'utf8mb4'}
        )

    @contextmanager
    def session(self, close_at_exit: bool = True) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            if close_at_exit:
                session.close()

    def get_engine(self) -> Engine:
        return self._engine

    def get_source_uri(self) -> URL:
        return self._source_uri

    @exception_handled
    def create(self, entity: BaseSchema, model_type: _ModelTypeT) -> Generic[_ModelTypeT]:
        with self.session() as session:
            new_entry: _ModelTypeT = model_type(**entity.get_json())
            session.add(new_entry)
            return new_entry

    @exception_handled
    def get_or_create(self, entity: BaseSchema, model_type: _ModelTypeT) -> Generic[_ModelTypeT]:
        with self.session() as session:
            existing_entry: model_type | None = session.query(model_type).filter_by(**entity.get_json()).one_or_none()
            if existing_entry:
                return existing_entry
            new_entry: _ModelTypeT = model_type(**entity.get_json())
            session.add(new_entry)
            return new_entry


databaseOperationsService = DatabaseOperationsService()
