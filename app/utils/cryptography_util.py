"""Cryptography utility used to hash and validate etc."""
from bcrypt import hashpw, gensalt, checkpw

class CryptographyUtil:
    @classmethod
    def salty_hash(cls, plain_text_password: bytes) -> bytes:
        salt: bytes = gensalt(12)
        return hashpw(password=plain_text_password, salt=salt)

    @classmethod
    def validate_password(cls, plain_text_password: bytes, password_hash: bytes) -> bool:
        return checkpw(password=plain_text_password, hashed_password=password_hash)
