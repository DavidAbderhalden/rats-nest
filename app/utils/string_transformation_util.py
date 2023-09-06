"""String utility module (transformation etc.)"""
import re
import random


UPPER_CASE_CHARACTERS: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_CASE_CHARACTERS: str = 'abcdefghijklmnopqrstuvwxyz'
DIGITS: str = '1234567890'
SPECIAL_CHARACTERS: str = '[-+_!@#$%^&*.,?]'

class StringTransformationUtil:
    @classmethod
    def pascal_to_snake_case(cls, pascal_string: str) -> str:
        words: list[str] = re.findall('[A-Z][^A-Z]*', pascal_string)
        return '_'.join(words).lower()

    @classmethod
    def create_random_code(
            cls,
            length: int = 10,
            upper_case: bool = True,
            lower_case: bool = True,
            digits: bool = False,
            specials: bool = False
    ) -> str:
        letters: str = ''
        if upper_case:
            letters += UPPER_CASE_CHARACTERS
        if lower_case:
            letters += LOWER_CASE_CHARACTERS
        if digits:
            letters += DIGITS
        if specials:
            letters += SPECIAL_CHARACTERS
        if letters == '':
            # TODO: Throw error or something
            return ''
        return ''.join(random.choice(letters) for i in range(length))
