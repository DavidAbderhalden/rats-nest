"""Service used for all database related operations"""
from typing import Callable, TypeVar, Generic

from contextlib import asynccontextmanager, AbstractAsyncContextManager

from sqlalchemy.pool import QueuePool
from sqlalchemy.future import select
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from app.environments.settings import settings as app_settings
from app.schemas import BaseSchema

_ModelTypeT = TypeVar('_ModelTypeT')


# TODO: Create email etc verification tables
class DatabaseOperationsService:
    _source_uri: URL
    _engine: AsyncEngine
    _session_factory: async_sessionmaker

    def __init__(self) -> None:
        self._source_uri: URL = self._create_source_uri()
        self._engine = create_async_engine(
            self._source_uri,
            pool_pre_ping=True,
            pool_recycle=90,
            pool_size=10,
            poolclass=QueuePool,
            echo=True
        )
        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=self._engine,
            expire_on_commit=False
        )

    @classmethod
    def _create_source_uri(cls) -> URL:
        return URL.create(
            drivername='mysql+aiomysql',
            username=app_settings.DATABASE_USER,
            password=app_settings.DATABASE_PASSWORD,
            host=app_settings.DATABASE_HOST,
            port=app_settings.DATABASE_PORT,
            database=app_settings.DATABASE_NAME,
            query={'charset': 'utf8mb4'}
        )

    @asynccontextmanager
    async def session(self, close_at_exit: bool = True) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            if close_at_exit:
                await session.close()

    def get_engine(self) -> AsyncEngine:
        return self._engine

    def get_source_uri(self) -> URL:
        return self._source_uri

    async def create(self, entity: BaseSchema, model_type: _ModelTypeT) -> Generic[_ModelTypeT]:
        async with self.session() as session:
            new_entry: _ModelTypeT = model_type(**entity.get_json())
            session.add(new_entry)
            await session.flush()
            await session.refresh(new_entry)
            return new_entry

    async def get_or_create(self, entity: BaseSchema, model_type: _ModelTypeT) -> Generic[_ModelTypeT]:
        async with self.session() as session:
            select_statement = select(model_type).filter_by(**entity.get_json())
            existing_entry: model_type | None = await session.scalars(select_statement)
            first_entry = existing_entry.first()
            if first_entry:
                return first_entry
            new_entry: _ModelTypeT = model_type(**entity.get_json())
            session.add(new_entry)
            await session.flush()
            await session.refresh(new_entry)
            return new_entry


database_operations_service = DatabaseOperationsService()