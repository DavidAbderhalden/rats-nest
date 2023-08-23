"""Database enumerations"""
from enum import StrEnum

class Roles(StrEnum):
    SUPER_ADMIN: str = 'super_admin'
    ADMIN: str = 'admin'
    SUPER_USER: str = 'super_user'
    USER: str = 'user'


class ProductCategories(StrEnum):
    RODENT: str = 'rodent'
    DOG: str = 'dog'
    CAT: str = 'cat'
    RABBIT: str = 'rabbit'
    SNAKE: str = 'snake'
    FOOD: str = 'food'
    TERRARIUM: str = 'terrarium'
    CAGE: str = 'cage'
    TOY: str = 'toy'
    MISC: str = 'misc'


class Countries(StrEnum):
    CH: str = 'ch'
    DE: str = 'de'
    IT: str = 'it'
    FR: str = 'fr'
    EN: str = 'en'
    US: str = 'us'
