from app.domain.exceptions import UsuarioNoEncontradoError
from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort

"""
UC4 — Obtener usuario por ID
"""


class ObtenerUsuarioPorIdUseCase:
    """
    UC4 — Consulta un usuario por su identificador.

    Attributes:
        _repo : UsuarioQueryPort
    """

    def __init__(self, repo: UsuarioQueryPort) -> None:
        self._repo = repo

    async def execute(self, usuario_id: int):
        """
        Raises:
            UsuarioNoEncontradoError — Si no existe un usuario con ese ID.
        """
        usuario = await self._repo.obtener_por_id(usuario_id)

        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe usuario con id={usuario_id}")

        return usuario
