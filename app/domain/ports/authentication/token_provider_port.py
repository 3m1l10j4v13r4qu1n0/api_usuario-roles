from abc import ABC, abstractmethod


class TokenProviderPort(ABC):
    """
    Puerto para la emisión y validación de tokens JWT.

    UC1 — Login
    Dependencia para proteger endpoints (get_current_user)
    """

    @abstractmethod
    def crear_token(self, usuario_id: int, roles: list[str]) -> str:
        """
        Genera un token JWT firmado con el id de usuario y sus roles.
        El vencimiento lo define la configuración (JWT_EXPIRATION_MINUTES).
        """
        ...

    @abstractmethod
    def decodificar_token(self, token: str) -> dict:
        """
        Valida la firma y el vencimiento de un token JWT.
        Devuelve el payload (dict) si es válido.

        Raises:
            TokenInvalidoError — Si el token es inválido o está vencido.
        """
        ...
