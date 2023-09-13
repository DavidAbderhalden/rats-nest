"""Service used for all database related operations"""
from typing import Callable, TypeVar, Generic, Any

from contextlib import asynccontextmanager, AbstractAsyncContextManager

from sqlalchemy import ScalarResult, ColumnElement, delete
from sqlalchemy.pool import QueuePool
from sqlalchemy.future import select
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from app.environments.settings import settings as app_settings
from app.schemas import BaseSchema
from app.models import (
    AddressModel,
    StreetsModel,
    CitiesModel,
    CustomersModel,
    ConfirmationCodesModel
)

_ModelTypeT = TypeVar('_ModelTypeT')


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
            echo=app_settings.ENVIRONMENT == 'development'
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
            scalar_result: ScalarResult[model_type] = await session.scalars(select_statement)
            entry_or_none: model_type | None = scalar_result.first()
            if entry_or_none:
                return entry_or_none
            new_entry: _ModelTypeT = model_type(**entity.get_json())
            session.add(new_entry)
            await session.flush()
            await session.refresh(new_entry)
            return new_entry

    async def get_or_throw(self, entity: BaseSchema, model_type: _ModelTypeT) -> Generic[_ModelTypeT]:
        async with self.session() as session:
            select_statement = select(model_type).filter_by(**entity.get_json())
            scalar_result: ScalarResult[model_type] = await session.scalars(select_statement)
            return scalar_result.one()

    async def get_by_id(self, entity_id: int, model_type: _ModelTypeT) -> _ModelTypeT | None:
        async with self.session() as session:
            select_statement = select(model_type).where(model_type.id == entity_id)
            scalar_result: ScalarResult[model_type] = await session.scalars(select_statement)
            return scalar_result.one_or_none()

    async def get_by_attribute_or_throw(
            self,
            value: Any,
            attr_name: str,
            model_type: _ModelTypeT
    ) -> Generic[_ModelTypeT]:
        async with self.session() as session:
            attribute = getattr(model_type, attr_name, ColumnElement[type(value)])
            select_statement = select(model_type).where(attribute == value)
            scalar_result: ScalarResult[model_type] = await session.scalars(select_statement)
            return scalar_result.one()

    async def get_by_attribute_or_none(
            self,
            value: Any,
            attr_name: str,
            model_type: _ModelTypeT
    ) -> Generic[_ModelTypeT]:
        async with self.session() as session:
            attribute = getattr(model_type, attr_name, ColumnElement[type(value)])
            select_statement = select(model_type).where(attribute == value)
            scalar_result: ScalarResult[model_type] = await session.scalars(select_statement)
            return scalar_result.one_or_none()
    async def delete_by_attribute_if_exists(
            self,
            value: Any,
            attr_name: str,
            model_type: _ModelTypeT
    ) -> None:
        async with self.session() as session:
            attribute = getattr(model_type, attr_name, ColumnElement[type(value)])
            delete_statement = delete(model_type).where(attribute == value)
            await session.execute(delete_statement)

    async def delete_attributes_or_throw(self, entity: BaseSchema, model_type: _ModelTypeT) -> Generic[_ModelTypeT]:
        async with self.session() as session:
            select_statement = select(model_type).filter_by(**entity.get_json())
            scalar_result: ScalarResult[model_type] = await session.scalars(select_statement)
            entry: model_type = scalar_result.one()
            for attribute, value in entity.__dict__.items():
                original_value: Any = getattr(entry, attribute)
                setattr(entry, attribute, None if value else original_value)
            await session.flush()
            await session.refresh(entry)
            return entry

    async def is_customer_verified(self, customer_id: int) -> bool:
        async with self.session() as session:
            select_statement = select(ConfirmationCodesModel).join(
                CustomersModel.customer_confirmation_codes_relationship).where(CustomersModel.id == customer_id)
            scalar_result: ScalarResult[ConfirmationCodesModel] = await session.scalars(select_statement)
            entry: ConfirmationCodesModel = scalar_result.one()
            return not entry.email_validation

    # FIXME: Make dynamic (get formatted or something like that)
    async def get_address_strings(self) -> list[str]:
        async with self.session() as session:
            select_statement = select(
                AddressModel.house_number.label('house_number'),
                StreetsModel.name.label('street_name'),
                CitiesModel.name.label('city_name'),
                CitiesModel.zip_code.label('zip_code'),
                CitiesModel.country.label('country_code')
            ).join(
                AddressModel.address_street_relationship
            ).join(
                StreetsModel.street_city_relationship
            )
            rows = await session.execute(select_statement)
            results = rows.mappings().all()
            return list(
                map(lambda x:
                    f'{x.zip_code} {x.city_name}, {x.street_name} {x.house_number} ({x.country_code.upper()})', results)
            )


database_operations_service = DatabaseOperationsService()
