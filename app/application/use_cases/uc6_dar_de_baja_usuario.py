from app.domain.exceptions import UsuarioNoEncontradoError
from app.domain.ports.authentication.estado_usuario_cache_port import (
    EstadoUsuarioCachePort,
)
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort

"""
UC6 — Dar de baja usuario
La baja es lógica: se marca activo = False, no se borra físicamente.
Al darlo de baja se invalida su estado en cache para revocarlo en caliente.
"""


class DarDeBajaUsuarioUseCase:
    """
    UC6 — Baja lógica de un usuario.

    Attributes:
        _repo : UsuarioCommandPort
        _estado_cache : EstadoUsuarioCachePort
    """

    def __init__(
        self,
        repo: UsuarioCommandPort,
        estado_cache: EstadoUsuarioCachePort,
    ) -> None:
        self._repo = repo
        self._estado_cache = estado_cache

    async def execute(self, usuario_id: int):
        usuario = await self._repo.dar_de_baja(usuario_id)

        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe usuario con id={usuario_id}")

        await self._estado_cache.invalidar(usuario_id)
        return usuario
