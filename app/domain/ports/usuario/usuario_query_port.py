from abc import ABC, abstractmethod

from app.domain.models.usuario import Usuario


class UsuarioQueryPort(ABC):
    """
    Puerto para CONSULTAS.

    UC1 — Login (obtener por email)
    UC3 — Listar usuarios
    UC4 — Obtener usuario por id
    get_current_user — Obtener usuario desde el token
    """

    @abstractmethod
    async def listar(self) -> list[Usuario]:
        """
        UC3 — Obtiene todos los usuarios almacenados.
        """
        ...

    @abstractmethod
    async def obtener_por_id(self, usuario_id: int) -> Usuario | None:
        """
        UC4 — Obtiene un usuario por su ID.
        Devuelve None si no existe.
        """
        ...

    @abstractmethod
    async def obtener_por_email(self, email: str) -> Usuario | None:
        """
        UC1 — Obtiene un usuario por su email.
        Devuelve None si no existe.
        """
        ...
