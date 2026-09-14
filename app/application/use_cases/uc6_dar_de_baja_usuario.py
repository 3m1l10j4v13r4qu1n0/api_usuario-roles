from app.domain.exceptions import UsuarioNoEncontradoError
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort

"""
UC6 — Dar de baja usuario
La baja es lógica: se marca activo = False, no se borra físicamente.
"""


class DarDeBajaUsuarioUseCase:
    """
    UC6 — Baja lógica de un usuario.

    Attributes:
        _repo : UsuarioCommandPort
    """

    def __init__(self, repo: UsuarioCommandPort) -> None:
        self._repo = repo

    async def execute(self, usuario_id: int):
        usuario = await self._repo.dar_de_baja(usuario_id)

        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe usuario con id={usuario_id}")

        return usuario
