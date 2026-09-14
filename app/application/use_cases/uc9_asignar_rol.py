from app.domain.exceptions import RolNoEncontradoError, UsuarioNoEncontradoError
from app.domain.ports.rol.rol_command_port import RolCommandPort
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort

"""
UC9 — Asignar rol
"""


class AsignarRolUseCase:
    """
    UC9 — Asigna un rol a un usuario.

    Attributes:
        _usuario_repo : UsuarioCommandPort
        _rol_repo : RolCommandPort
    """

    def __init__(
        self,
        usuario_repo: UsuarioCommandPort,
        rol_repo: RolCommandPort,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._rol_repo = rol_repo

    async def execute(self, usuario_id: int, rol_id: int):
        """
        Raises:
            RolNoEncontradoError — Si el rol no existe.
            UsuarioNoEncontradoError — Si el usuario no existe.
        """
        rol = await self._rol_repo.buscar_por_id(rol_id)
        if rol is None:
            raise RolNoEncontradoError(f"No existe rol con id={rol_id}")

        usuario = await self._usuario_repo.asignar_rol(usuario_id, rol_id)

        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe usuario con id={usuario_id}")

        return usuario
