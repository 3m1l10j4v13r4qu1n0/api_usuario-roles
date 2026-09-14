from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort

"""
UC3 — Listar usuarios
"""


class ListarUsuariosUseCase:
    """
    UC3 — Obtiene todos los usuarios almacenados.

    Attributes:
        _repo : UsuarioQueryPort
    """

    def __init__(self, repo: UsuarioQueryPort) -> None:
        self._repo = repo

    async def execute(self) -> list:
        return await self._repo.listar()
