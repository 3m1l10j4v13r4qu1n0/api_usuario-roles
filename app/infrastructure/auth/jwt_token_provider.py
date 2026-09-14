from datetime import UTC, datetime, timedelta

import jwt

from app.domain.exceptions import TokenInvalidoError
from app.domain.ports.authentication.token_provider_port import TokenProviderPort
from app.infrastructure.core.config import settings


class JwtTokenProvider(TokenProviderPort):
    """
    Adapter de emisión/validación de tokens JWT con PyJWT.
    """

    def crear_token(self, usuario_id: int, roles: list[str]) -> str:
        ahora = datetime.now(UTC)
        payload = {
            "sub": str(usuario_id),
            "roles": roles,
            "iat": ahora,
            "exp": ahora + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def decodificar_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.InvalidTokenError:
            raise TokenInvalidoError()
