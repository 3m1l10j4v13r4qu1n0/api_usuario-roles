from abc import ABC, abstractmethod

from app.domain.models.rol import Rol


class RolCommandPort(ABC):
    """
    Puerto para ESCRITURA.

    UC7 — Crear rol
    UC9 — Verificar rol al asignarlo
    """

    @abstractmethod
    async def crear(self, rol: Rol) -> Rol:
        """
        UC7 — Persiste un rol nuevo.
        """
        ...

    @abstractmethod
    async def buscar_por_id(self, rol_id: int) -> Rol | None:
        """
        UC9 — Busca un rol por su ID. Devuelve None si no existe.
        """
        ...

    @abstractmethod
    async def buscar_por_nombre(self, nombre: str) -> Rol | None:
        """
        UC7 — Verifica si ya existe un rol con ese nombre.
        Devuelve None si no existe.
        """
        ...
