from cachetools import TTLCache

from app.domain.models.estado_usuario import EstadoUsuario
from app.domain.ports.authentication.estado_usuario_cache_port import (
    EstadoUsuarioCachePort,
)
from app.infrastructure.core.config import settings


class EstadoUsuarioCacheMemoria(EstadoUsuarioCachePort):
    """
    Adapter de cache en memoria con TTL corto (cachetools.TTLCache).

    Scope académico/simple: la entrada vive solo dentro del proceso. No se
    comparte entre réplicas si se escala horizontalmente (para eso haría
    falta Redis, ver port `EstadoUsuarioCachePort`).
    """

    def __init__(self) -> None:
        self._cache: TTLCache[int, EstadoUsuario] = TTLCache(
            maxsize=settings.AUTH_CACHE_MAX_ITEMS,
            ttl=settings.AUTH_CACHE_TTL_SEGUNDOS,
        )

    async def obtener(self, usuario_id: int) -> EstadoUsuario | None:
        return self._cache.get(usuario_id)

    async def guardar(self, estado: EstadoUsuario) -> None:
        self._cache[estado.usuario_id] = estado

    async def invalidar(self, usuario_id: int) -> None:
        self._cache.pop(usuario_id, None)
