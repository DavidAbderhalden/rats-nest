"""The sqlalchemy base model"""
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.utils import pascal_to_snake_case


class BaseModel(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        table_name: str = self.__name__.split('Model', 1)[0]
        return pascal_to_snake_case(table_name)
