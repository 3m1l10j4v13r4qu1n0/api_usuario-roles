from app.domain.exceptions import RolNoEncontradoError, UsuarioNoEncontradoError
from app.domain.ports.authentication.estado_usuario_cache_port import (
    EstadoUsuarioCachePort,
)
from app.domain.ports.rol.rol_command_port import RolCommandPort
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort

"""
UC10 — Quitar rol
Al quitar el rol se invalida el estado en cache para revocar la
autorización en caliente (sin esperar la expiración del JWT).
"""


class QuitarRolUseCase:
    """
    UC10 — Quita un rol a un usuario.

    Attributes:
        _usuario_repo : UsuarioCommandPort
        _rol_repo : RolCommandPort
        _estado_cache : EstadoUsuarioCachePort
    """

    def __init__(
        self,
        usuario_repo: UsuarioCommandPort,
        rol_repo: RolCommandPort,
        estado_cache: EstadoUsuarioCachePort,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._rol_repo = rol_repo
        self._estado_cache = estado_cache

    async def execute(self, usuario_id: int, rol_id: int):
        """
        Raises:
            RolNoEncontradoError — Si el rol no existe.
            UsuarioNoEncontradoError — Si el usuario no existe.
        """
        rol = await self._rol_repo.buscar_por_id(rol_id)
        if rol is None:
            raise RolNoEncontradoError(f"No existe rol con id={rol_id}")

        usuario = await self._usuario_repo.quitar_rol(usuario_id, rol_id)

        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe usuario con id={usuario_id}")

        await self._estado_cache.invalidar(usuario_id)
        return usuario
