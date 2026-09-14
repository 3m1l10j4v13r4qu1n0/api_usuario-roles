import bcrypt

from app.domain.ports.authentication.password_hasher_port import PasswordHasherPort
from app.infrastructure.core.config import settings


class BcryptPasswordHasher(PasswordHasherPort):
    """
    Adapter del hashing de contraseñas con bcrypt.
    """

    def __init__(self, rounds: int = 12) -> None:
        self._rounds = rounds

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=self._rounds)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8"),
            )
        except ValueError:
            return False


def build_hasher() -> BcryptPasswordHasher:
    """Factory para el contenedor de dependencias."""
    # DEBUG=True y rounds bajos: instancias rapidas en local.dev
    return BcryptPasswordHasher(rounds=4 if settings.DEBUG else 12)
