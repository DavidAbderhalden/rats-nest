"""Service that handles everything behind jwt creation and parsing"""
from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError

from app.schemas import BaseSchema

from app.environments import settings

class TokenPayload(BaseSchema):
    auth_token: str

class JwtService:
    # in minutes
    _ACCESS_TOKEN_VALIDITY_DELTA: int = 15
    _REFRESH_TOKEN_VALIDITY_DELTA: int = 10080
    _JWT_ENCODING_ALGORITHM: str = 'HS256'


    def generate_access_token(self, data: TokenPayload) -> str:
        return self.generate_token(data, self._ACCESS_TOKEN_VALIDITY_DELTA)

    def generate_refresh_token(self, data: TokenPayload) -> str:
        return self.generate_token(data, self._REFRESH_TOKEN_VALIDITY_DELTA)

    def generate_token(self, data: TokenPayload, expiry_delta: int) -> str:
        jwt_data: dict = data.get_json().copy()
        expires: datetime = datetime.now(timezone.utc) + timedelta(minutes=expiry_delta)
        jwt_data.update({'exp': expires})
        return jwt.encode(jwt_data, settings.JWT_SECRET_KEY, algorithm=self._JWT_ENCODING_ALGORITHM)

    def validate_token(self, token: str) -> TokenPayload | None:
        try:
            return TokenPayload(**jwt.decode(token, key=settings.JWT_SECRET_KEY))
        except JWTError:
            return None

    @classmethod
    def get_token_expiration_date(cls, token: str) -> datetime:
        return jwt.decode(token, key=settings.JWT_SECRET_KEY).get('exp')

    def get_access_token_validity_delta_seconds(self) -> int:
        return self._ACCESS_TOKEN_VALIDITY_DELTA * 60

    def get_refresh_token_validity_delta_seconds(self) -> int:
        return self._REFRESH_TOKEN_VALIDITY_DELTA * 60


jwt_service: JwtService = JwtService()
