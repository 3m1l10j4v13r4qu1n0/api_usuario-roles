from abc import ABC, abstractmethod

from app.domain.models.estado_usuario import EstadoUsuario


class EstadoUsuarioCachePort(ABC):
    """
    Puerto para el cache de estado del usuario autenticado.

    Almacena por un TTL corto los datos que la autorización necesita
    (activo + roles) para evitar consultar la BD en cada request.

    Patrón híbrido: access token JWT de vida corta + cache de estado
    con TTL. La revocación se logra invalidando la entrada.
    """

    @abstractmethod
    async def obtener(self, usuario_id: int) -> EstadoUsuario | None:
        """
        Devuelve el estado del usuario si hay una entrada vigente en cache.
        Devuelve None si no hay nada (miss) → debe recargarse desde la BD.
        """
        ...

    @abstractmethod
    async def guardar(self, estado: EstadoUsuario) -> None:
        """
        Guarda/refresca el estado del usuario en cache.
        """
        ...

    @abstractmethod
    async def invalidar(self, usuario_id: int) -> None:
        """
        Invalida la entrada del usuario para que el próximo request la
        recargue desde la BD (revocación inmediata de rol/acceso).
        """
        ...
