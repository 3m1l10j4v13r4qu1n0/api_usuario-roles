from abc import ABC, abstractmethod

from app.domain.models.rol import Rol


class RolQueryPort(ABC):
    """
    Puerto para CONSULTAS.

    UC8 — Listar roles
    """

    @abstractmethod
    async def listar(self) -> list[Rol]:
        """
        UC8 — Obtiene todos los roles almacenados.
        """
        ...

    @abstractmethod
    async def obtener_nombres_por_ids(self, ids_roles: list[int]) -> list[str]:
        """
        UC1 — Resuelve los nombres de los roles a partir de sus IDs,
        para armar el payload del token JWT.
        """
        ...
