from abc import ABC, abstractmethod

from app.domain.models.usuario import Usuario


class UsuarioCommandPort(ABC):
    """
    Puerto para ESCRITURA.

    UC2 — Registrar usuario
    UC5 — Actualizar usuario
    UC6 — Dar de baja usuario
    UC9 — Asignar rol
    UC10 — Quitar rol
    """

    @abstractmethod
    async def crear(self, usuario: Usuario) -> Usuario:
        """
        UC2 — Persiste un usuario nuevo.
        """
        ...

    @abstractmethod
    async def actualizar(self, usuario_id: int, campos: dict) -> Usuario | None:
        """
        UC5 — Actualiza solo los campos indicados.
        Devuelve None si el usuario no existe.
        """
        ...

    @abstractmethod
    async def dar_de_baja(self, usuario_id: int) -> Usuario | None:
        """
        UC6 — Baja lógica: marca activo = False.
        Devuelve None si el usuario no existe.
        """
        ...

    @abstractmethod
    async def asignar_rol(self, usuario_id: int, rol_id: int) -> Usuario | None:
        """
        UC9 — Asigna un rol a un usuario.
        Devuelve None si el usuario no existe.
        """
        ...

    @abstractmethod
    async def quitar_rol(self, usuario_id: int, rol_id: int) -> Usuario | None:
        """
        UC10 — Quita un rol a un usuario.
        Devuelve None si el usuario no existe.
        """
        ...

    @abstractmethod
    async def buscar_por_email(self, email: str) -> Usuario | None:
        """
        UC2 — Verifica si el email ya está registrado.
        Devuelve None si no existe.
        """
        ...

    @abstractmethod
    async def buscar_por_email_excluyendo_id(
        self, email: str, usuario_id: int
    ) -> Usuario | None:
        """
        UC5 — Verifica si el email está en uso por OTRO usuario.
        """
        ...
