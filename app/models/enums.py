"""Database enumerations"""
from enum import IntEnum, StrEnum

class Roles(IntEnum):
    SUPER_ADMIN: str = 3
    ADMIN: str = 2
    SUPER_USER: str = 1
    USER: str = 0

    def superior_or_equal(self, base_role: IntEnum):
        return self.value >= base_role.value

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
