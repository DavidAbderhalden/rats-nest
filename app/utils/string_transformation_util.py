"""String utility module (transformation etc.)"""
import re

def pascal_to_snake_case(pascal_string: str) -> str:
    words: list[str] = re.findall('[A-Z][^A-Z]*', pascal_string)
    return '_'.join(words).lower()
