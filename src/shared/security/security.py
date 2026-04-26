from datetime import datetime, timedelta, timezone
from shared.security.dto import SubTokenPayloadDTO
from shared.config import settings
import shared.exceptions as exc
from uuid import UUID
import jwt


class Security:

    @staticmethod
    def create_token(
        payload: SubTokenPayloadDTO,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        if expire_timedelta is None:
            expire_timedelta: timedelta = settings.jwt.expire_timedelta

        now = datetime.now(timezone.utc)

        to_encode = {
            "sub": str(payload.sub),
            "exp": now + expire_timedelta,
            "iat": now,
        }

        return jwt.encode(
            to_encode,
            settings.jwt.secret_key,
            algorithm=settings.jwt.algorithm,
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.jwt.secret_key,
                algorithms=[settings.jwt.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise exc.TokenExpiredException
        except jwt.InvalidTokenError:
            raise exc.InvalidTokenException

    @staticmethod
    def validate_exp(payload: dict) -> dict:
        exp = payload.get("exp")

        if exp is None:
            raise exc.InvalidTokenException

        exp_dt = datetime.fromtimestamp(float(exp), tz=timezone.utc)

        if exp_dt < datetime.now(timezone.utc):
            raise exc.TokenExpiredException

        return payload

    @staticmethod
    def extract_sub(payload: dict) -> SubTokenPayloadDTO:
        sub = payload.get("sub")

        if not sub:
            raise exc.InvalidTokenException

        return SubTokenPayloadDTO(sub=UUID(sub))
